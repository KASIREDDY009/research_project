#!/usr/bin/env python3
"""Score the BGL-trained baseline, as configured, on the LogHub pairs BGL -> HDFS and BGL -> OpenStack.

Each target is split chronologically in half: the first half's normal lines are the fault-free window,
whose later half sets the alarm threshold as in the evaluation, and the second half is scored (HDFS also per block session). F1, MCC, AUC,
precision, recall and false-alarm rate are reported beside the values published for ELFA-Log.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]

from sflad.data.loghub import load_bgl, load_hdfs, load_openstack, split_chronological  # noqa: E402
from sflad.pipeline.metrics import false_alarm_rate, precision_recall_f1  # noqa: E402
from sflad.pipeline.train_eval import load_config, transfer_detector  # noqa: E402

# Published reference values per pair: F1 in per cent, MCC.
ELFA_LOG_TABLE2 = {
    "BGL->HDFS": {"f1": 71.83, "mcc": 0.674},
    "BGL->OpenStack": {"f1": 58.43, "mcc": 0.054},
}
# Published reference log message and anomaly counts per corpus.
ELFA_LOG_TABLE1 = {
    "BGL": {"messages": 4_747_963, "anomalies": 348_460},
    "HDFS": {"messages": 5_000_000, "anomalies": 284_818},
    "OpenStack": {"messages": 70_724, "anomalies": 18_435},
}

_BLOCK = re.compile(r"blk_-?\d+")


def _metrics(y_true, y_pred, scores) -> dict:
    m = precision_recall_f1(y_true, y_pred)
    both = 0 < int(np.sum(y_true)) < len(y_true)
    return {
        **{k: m[k] for k in ("precision", "recall", "f1", "mcc", "tp", "fp", "fn", "tn")},
        "auc": float(roc_auc_score(y_true, scores)) if both else float("nan"),
        "false_alarm_rate": false_alarm_rate(y_true, y_pred),
    }


def _block_scores(det, eval_events) -> dict:
    """Score each HDFS block session: highest window score, any window alarm, block label."""
    sessions: dict = {}
    for e in eval_events:
        found = _BLOCK.search(e.message)
        if found:
            sessions.setdefault(found.group(0), []).append(e)
    y_true, y_pred, scores = [], [], []
    for lines in sessions.values():
        res = det.predict([replace(e, split="eval") for e in lines])
        y_true.append(int(any(e.is_anomaly for e in lines)))
        y_pred.append(int(res.y_pred.any()))
        scores.append(float(res.scores.max()))
    return {**_metrics(np.array(y_true), np.array(y_pred), np.array(scores)), "n_blocks": len(y_true)}


def run_pair(cfg: dict, source, target, window: int, step: int, seed: int, per_block: bool = False) -> dict:
    target = split_chronological(target, 0.5)
    fault_free = [e for e in target if e.split == "eval" or not e.is_anomaly]
    evals = [e for e in target if e.split == "eval"]
    det = transfer_detector(cfg, window, step, random_state=seed)
    res = det.fit(fault_free, source_events=source).predict(target)
    out = {**_metrics(res.y_true, res.y_pred, res.scores), "meta": res.meta}
    if per_block:
        out["per_block"] = _block_scores(det, evals)
    return out


def _counts(name: str, events) -> dict:
    return {"events": len(events), "anomalous_events": int(sum(e.is_anomaly for e in events)),
            "elfa_log": ELFA_LOG_TABLE1[name]}


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _fmt(x: float, scale: float = 1.0, digits: int = 2) -> str:
    return "n/a" if x != x else f"{scale * x:.{digits}f}"


def run(a: argparse.Namespace, cfg: dict) -> dict:
    """Calibration results for the requested pairs."""
    source = load_bgl(a.bgl, max_lines=a.bgl_lines)
    corpora = {"BGL": _counts("BGL", source)}
    inputs = [a.bgl]
    results = {}
    for pair in a.pairs:
        if pair == "HDFS":
            target = load_hdfs(a.hdfs_log, a.hdfs_labels, max_lines=a.hdfs_lines, group_by_block=True)
            inputs += [a.hdfs_log, a.hdfs_labels]
        else:
            abnormal = a.openstack_dir / "openstack_abnormal.log"
            logs = [a.openstack_dir / "openstack_normal1.log", abnormal]
            target = load_openstack(logs, a.openstack_dir / "anomaly_labels.txt", anomalous_files=[abnormal])
            inputs += logs + [a.openstack_dir / "anomaly_labels.txt"]
        corpora[pair] = _counts(pair, target)
        key = f"BGL->{pair}"
        results[key] = {
            "elfa_log_reference": ELFA_LOG_TABLE2[key],
            "n_target_events": len(target),
            "n_target_anomalous_events": int(sum(e.is_anomaly for e in target)),
            "baseline": run_pair(cfg, source, target, a.window, a.step, a.seed, per_block=pair == "HDFS"),
        }
        del target
    settings = {"inputs": {p.name: _sha256(p) for p in inputs}, "bgl_lines": a.bgl_lines, "hdfs_lines": a.hdfs_lines,
                "window": a.window, "step": a.step, "seed": a.seed}
    return {"results": results, "corpora": corpora, "settings": settings}


def merge(parts: list) -> dict:
    """One calibration from parts that ran different pairs with the same settings."""
    shared = [{k: v for k, v in part["settings"].items() if k != "inputs"} for part in parts]
    if any(s != shared[0] for s in shared):
        raise ValueError("calibration parts were run with different settings")
    merged = {"results": {}, "corpora": {}, "settings": {**shared[0], "inputs": {}}}
    for part in parts:
        merged["settings"]["inputs"].update(part["settings"]["inputs"])
        merged["corpora"].update(part["corpora"])
        merged["results"].update(part["results"])
    merged["results"] = {pair: merged["results"][pair] for pair in ELFA_LOG_TABLE2 if pair in merged["results"]}
    return merged


def render(cal: dict) -> str:
    s = cal["settings"]
    lines = [
        "# BGL-trained baseline on public LogHub transfer pairs",
        "",
        f"Window {s['window']}, step {s['step']}; seed {s['seed']}; the baseline as configured for the evaluation. "
        "Targets are split chronologically in half and the second half is scored; the later half of the first half's normal "
        "lines sets the alarm threshold, as in the evaluation. HDFS lines are grouped by block session; every line of openstack_abnormal.log "
        "counts as an anomaly.",
        "",
        "| Corpus | Lines used | Anomalous lines | ELFA-Log messages | ELFA-Log anomalies |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, d in cal["corpora"].items():
        lines.append(f"| {name} | {d['events']:,} | {d['anomalous_events']:,} | "
                     f"{d['elfa_log']['messages']:,} | {d['elfa_log']['anomalies']:,} |")
    lines += [
        "",
        "ELFA-Log is a deep model with domain-adversarial alignment, evaluated under its own protocol; its values",
        "are shown for comparison of scale only.",
        "",
        "| Pair | F1 (%) | MCC | AUC | Precision | Recall | FAR | ELFA-Log F1 (%) | ELFA-Log MCC |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for pair, r in cal["results"].items():
        ref = r["elfa_log_reference"]
        v = r["baseline"]
        lines.append(
            f"| {pair} | {_fmt(v['f1'], 100)} | {_fmt(v['mcc'], 1, 3)} | {_fmt(v['auc'], 1, 3)} | "
            f"{_fmt(v['precision'])} | {_fmt(v['recall'])} | {_fmt(v['false_alarm_rate'], 1, 3)} | "
            f"{ref['f1']:.2f} | {ref['mcc']:.3f} |"
        )
    if "BGL->HDFS" in cal["results"]:
        lines += [
            "",
            "HDFS scored per block session (a block alarms when any of its windows alarms):",
            "",
            "| Blocks | F1 (%) | MCC | AUC | Precision | Recall | FAR |",
            "|---:|---:|---:|---:|---:|---:|---:|",
        ]
        b = cal["results"]["BGL->HDFS"]["baseline"]["per_block"]
        lines.append(
            f"| {b['n_blocks']} | {_fmt(b['f1'], 100)} | {_fmt(b['mcc'], 1, 3)} | {_fmt(b['auc'], 1, 3)} | "
            f"{_fmt(b['precision'])} | {_fmt(b['recall'])} | {_fmt(b['false_alarm_rate'], 1, 3)} |"
        )
    lines += ["", "n/a marks an undefined value (for example precision when no alarm was raised)."]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    cfg = load_config(ROOT / "configs" / "default.yaml")
    full = ROOT / "data" / "public_corpus" / "full"
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--bgl", type=Path, default=full / "BGL.log")
    p.add_argument("--hdfs-log", type=Path, default=full / "HDFS.log")
    p.add_argument("--hdfs-labels", type=Path, default=full / "preprocessed" / "anomaly_label.csv")
    p.add_argument("--openstack-dir", type=Path, default=full)
    p.add_argument("--bgl-lines", type=int, default=None, help="BGL lines to read (default: all)")
    p.add_argument("--hdfs-lines", type=int, default=ELFA_LOG_TABLE1["HDFS"]["messages"],
                   help="HDFS lines to read (default: the size of ELFA-Log's HDFS set)")
    p.add_argument("--window", type=int, default=int(cfg["features"]["window_size"]))
    p.add_argument("--step", type=int, default=int(cfg["features"]["step_size"]))
    p.add_argument("--seed", type=int, default=int(cfg["seed"]))
    p.add_argument("--pairs", nargs="+", choices=["HDFS", "OpenStack"], default=["HDFS", "OpenStack"])
    p.add_argument("--merge", nargs="+", type=Path, help="calibration.json files of parts to combine instead of running")
    p.add_argument("--out", type=Path, default=ROOT / "results" / "calibration")
    a = p.parse_args(argv)

    cal = merge([json.loads(path.read_text()) for path in a.merge]) if a.merge else run(a, cfg)
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "calibration.json").write_text(json.dumps(cal, indent=2, default=str))
    md = render(cal)
    (a.out / "calibration.md").write_text(md)
    print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
