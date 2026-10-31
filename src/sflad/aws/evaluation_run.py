"""One evaluation run on one application, then its labelled CloudWatch export.

Phases: a fault-free training window with a sham configuration update every few cycles; fault
episodes of every category in one seeded shuffled order, each restored and followed by clean traffic;
and a fault-free elasticity window of concurrent bursts. An interrupt restores the deployed settings.
The slow limit (the slowest training-window call plus a margin) is fixed when the training window ends.

Usage: python -m sflad.aws.evaluation_run --app orders --out results/runs/<tag>/orders --seed 1
"""

from __future__ import annotations

import argparse
import json
import random
import signal
import subprocess
import threading
import time
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

import yaml
from botocore.config import Config

from sflad.aws.clients import make_client
from sflad.aws.collect_logs import IncompleteExportError, export_events, label_events
from sflad.aws.faults import Faults
from sflad.aws.workload import create_burst, failed, fault_reasons, faulty, latency_ms, normal_traffic


def _now_ms() -> int:
    return int(time.time() * 1000)


def terraform_apps(terraform_dir: Path) -> Dict[str, Any]:
    out = subprocess.run(["terraform", f"-chdir={terraform_dir}", "output", "-json", "apps"],
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def redact(text: str, account: str) -> str:
    """The text with the AWS account id replaced by <ACCOUNT>."""
    return text.replace(account, "<ACCOUNT>")


def run_evaluation(app_name: str, app: Dict[str, Any], cfg: Dict[str, Any], seed: int, raw_dir: Path,
                 lam, invoker, account: str) -> Dict[str, Any]:
    """Run the evaluation. lam changes the function's configuration; invoker calls the function; the
    account id is replaced by <ACCOUNT> in the saved run record."""
    wl, fc, cc = cfg["workload"], cfg["faults"], cfg["control"]
    rng = random.Random(seed)
    pause = float(wl["pause_seconds"])
    faults = Faults(lam, app, fc)
    order = [(category, i) for category in fc["categories"] for i in range(int(fc["injections_per_category"]))]
    rng.shuffle(order)
    slow_limit: Dict[str, int] = {}
    records: List[dict] = []
    episodes: List[dict] = []
    times: Dict[str, int] = {}

    def save_meta() -> None:
        (raw_dir / "run.json").write_text(redact(json.dumps(
            {"app": app_name, "seed": seed, "episode_order": [f"{c}-{i:02d}" for c, i in order],
             "slow_limit_ms": slow_limit.get("ms"), "times": times, "config": cfg, "deployed": app},
            indent=2), account))

    invocation_log = (raw_dir / "invocations.jsonl").open("a")
    episode_log = (raw_dir / "episodes.jsonl").open("a")
    lock = threading.Lock()

    def keep(record: dict) -> None:
        """Write each call the moment it returns, so a crash never loses a call that ran."""
        with lock:
            invocation_log.write(json.dumps(record) + "\n")
            invocation_log.flush()
            records.append(record)

    faults.restore_all()
    try:
        times["start"] = _now_ms()
        save_meta()
        every = int(wl["train_sham_every_cycles"])
        for done in range(0, int(wl["train_cycles"]), every):
            n = min(every, int(wl["train_cycles"]) - done)
            normal_traffic(invoker, app_name, app, n, rng, pause, {"phase": "train"}, on_record=keep)
            faults.sham()
        times["train_end"] = _now_ms()
        slow_limit["ms"] = max(latency_ms(r) for r in records) + int(cfg["labels"]["slow_margin_ms"])
        save_meta()
        print(f"training window: {len(records)} invocations; slow limit {slow_limit['ms']} ms", flush=True)
        limit = slow_limit["ms"]
        for category, i in order:
            labels = {"category": category, "episode": f"{category}-{i:02d}"}
            strength = faults.strength(category, i)
            if strength is not None:
                labels["strength_ms"] = strength
            inject_ms = _now_ms()
            faults.inject(category, i)
            burst = create_burst(invoker, app_name, app, int(wl["fault_burst"]), rng,
                                 {"phase": "fault", **labels}, on_record=keep)
            faults.restore_all()
            restored_ms = _now_ms()
            faults.sham()
            gap = normal_traffic(invoker, app_name, app, int(wl["gap_cycles"]), rng, pause,
                                 {"phase": "gap", **labels}, on_record=keep)
            episode = {**labels, "inject_ms": inject_ms, "restored_ms": restored_ms,
                       "burst": len(burst), "burst_faulty": sum(faulty(r, limit) for r in burst),
                       "gap_faulty": sum(faulty(r, limit) for r in gap)}
            episodes.append(episode)
            episode_log.write(json.dumps(episode) + "\n")
            episode_log.flush()
            print(f"{labels['episode']}: {episode['burst_faulty']}/{episode['burst']} fault calls faulty, "
                  f"{episode['gap_faulty']} gap calls faulty", flush=True)
        times["control_start"] = _now_ms()
        save_meta()
        for _ in range(int(cc["bursts"])):
            faults.sham()
            create_burst(invoker, app_name, app, int(cc["burst_concurrency"]), rng, {"phase": "control"},
                         concurrent=True, on_record=keep)
            normal_traffic(invoker, app_name, app, int(cc["cycles_between_bursts"]), rng, pause,
                           {"phase": "control"}, on_record=keep)
            time.sleep(float(cc["idle_seconds"]))
        times["end"] = _now_ms()
        print(f"elasticity window done: {len(records)} invocations in total", flush=True)
    finally:
        faults.restore_all()
        invocation_log.close()
        episode_log.close()
        save_meta()
    return {"times": times, "records": records, "episodes": episodes, "slow_limit_ms": slow_limit["ms"]}


def summarise_export(records: List[dict], episodes: List[dict], events, n_exported: int,
                     slow_limit_ms: int) -> Dict[str, Any]:
    """Run counts: faulty calls per phase and per reason, episodes per category with no or some faulty
    calls, orphan lines, and exported lines without text (which are not labelled or scored)."""
    by_category: Dict[str, Counter] = {}
    for ep in episodes:
        c = by_category.setdefault(ep["category"], Counter())
        c["episodes"] += 1
        c["silent"] += ep["burst_faulty"] == 0
        c["partial"] += 0 < ep["burst_faulty"] < ep["burst"]
    reasons = Counter()
    for r in records:
        for reason in fault_reasons(r, slow_limit_ms):
            reasons[f"{r['phase']}:{reason}"] += 1
    return {
        "invocations": len(records),
        "slow_limit_ms": slow_limit_ms,
        "faulty_invocations": dict(Counter(r["phase"] for r in records if faulty(r, slow_limit_ms))),
        "fault_reasons": dict(sorted(reasons.items())),
        "failed_invocations": dict(Counter(r["phase"] for r in records if failed(r))),
        "resent_calls": sum(r["resent"] > 0 for r in records),
        "exported_lines": n_exported,
        "blank_lines": n_exported - len(events),
        "lines": len(events),
        "anomalous_lines": sum(e.is_anomaly for e in events),
        "orphan_lines": dict(Counter(e.meta["phase"] for e in events if e.meta["orphan"])),
        "episodes": {cat: dict(c) for cat, c in by_category.items()},
    }


def export_run(app: Dict[str, Any], cfg: Dict[str, Any], raw_dir: Path, records, episodes, times, account: str,
               slow_limit_ms: int):
    """Save the raw export with the account id replaced by <ACCOUNT>, then label it, waiting for CloudWatch
    until every invocation's REPORT arrived."""
    ex = cfg["export"]
    for attempt in range(int(ex["attempts"])):
        time.sleep(float(ex["wait_seconds"]))
        raw = export_events(app["log_group"], times["start"] - 5000, _now_ms(), region=cfg["region"])
        for e in raw:
            e["message"] = redact(e["message"], account)
        with (raw_dir / "cloudwatch_events.jsonl").open("w") as f:
            for e in raw:
                f.write(json.dumps(e) + "\n")
        try:
            return label_events(raw, records, app["log_group"], times, episodes, slow_limit_ms)
        except IncompleteExportError:
            if attempt == int(ex["attempts"]) - 1:
                raise


def deployment_record(app: Dict[str, Any], region: str) -> Dict[str, Any]:
    """When the log group was created and when the function was last modified."""
    groups = make_client("logs", region=region).describe_log_groups(logGroupNamePrefix=app["log_group"])["logGroups"]
    function = make_client("lambda", region=region).get_function_configuration(FunctionName=app["function_name"])
    return {
        "log_group_created_ms": next(g["creationTime"] for g in groups if g["logGroupName"] == app["log_group"]),
        "function_last_modified": function["LastModified"],
    }


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--app", required=True, choices=["orders", "bookings"])
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--config", type=Path, default=Path("configs/aws.yaml"))
    a = p.parse_args(argv)
    cfg = yaml.safe_load(a.config.read_text())
    app = terraform_apps(Path(cfg["terraform_dir"]))[a.app]
    raw_dir = a.out / "raw"
    raw_dir.mkdir(parents=True, exist_ok=False)
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, signal.default_int_handler)
    region = cfg["region"]
    (raw_dir / "deployment.json").write_text(json.dumps(deployment_record(app, region), indent=2))
    account = make_client("sts", region=region).get_caller_identity()["Account"]
    result = run_evaluation(
        a.app, app, cfg, a.seed, raw_dir,
        lam=make_client("lambda", region=region),
        # A call is never sent twice by botocore: one that timed out may have run already.
        invoker=make_client("lambda", region=region, config=Config(retries={"total_max_attempts": 1},
                                                                    read_timeout=120)),
        account=account,
    )
    times, records, episodes = result["times"], result["records"], result["episodes"]
    events = export_run(app, cfg, raw_dir, records, episodes, times, account, result["slow_limit_ms"])
    with (raw_dir / "events.jsonl").open("w") as f:
        for ev in events:
            f.write(json.dumps(ev.to_dict()) + "\n")
    n_exported = sum(1 for _ in (raw_dir / "cloudwatch_events.jsonl").open())
    summary = summarise_export(records, episodes, events, n_exported, result["slow_limit_ms"])
    (raw_dir / "export.json").write_text(json.dumps(summary, indent=2))
    print(f"{a.app}: {summary['invocations']} invocations, {summary['lines']} log lines -> {raw_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
