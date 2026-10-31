"""Every evaluation run of one application side by side, as comparison.json and comparison.md.

Usage: python -m sflad.pipeline.comparison OUT_DIR RUN_DIR [RUN_DIR ...]
Each run folder holds raw/run.json, raw/episodes.jsonl and processed/results.json.
"""

from __future__ import annotations

import json
import math
import statistics
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

METRICS = ("precision", "recall", "f1", "mcc", "false_alarm_rate")


def describe(values: Sequence[float]) -> Dict[str, Any]:
    """Mean, spread and range over the defined values; NaN marks an undefined metric and is counted,
    not averaged. The spread needs at least two defined values."""
    defined = [v for v in values if not math.isnan(v)]
    return {
        "mean": statistics.mean(defined) if defined else None,
        "std": statistics.stdev(defined) if len(defined) > 1 else None,
        "min": min(defined) if defined else None,
        "max": max(defined) if defined else None,
        "n": len(defined),
        "n_undefined": len(values) - len(defined),
    }


def _fmt(value: Optional[float]) -> str:
    return "—" if value is None else f"{value:.4f}"


def compare_runs(out_dir: Path, run_dirs: Sequence[Path]) -> Dict[str, Any]:
    per_run: List[Dict[str, Any]] = []
    configs = []
    for rd in run_dirs:
        payload = json.loads((rd / "processed" / "results.json").read_text(encoding="utf-8"))
        configs.append(payload["config"])
        faults = json.loads((rd / "raw" / "run.json").read_text(encoding="utf-8"))["config"]["faults"]
        episodes = [json.loads(line) for line in (rd / "raw" / "episodes.jsonl").read_text().splitlines() if line]
        per_run.append({
            "run": f"{rd.parent.name}/{rd.name}",
            "injections_per_category": int(faults["injections_per_category"]),
            "categories": list(faults["categories"]),
            "n_fault_episodes": len(episodes),
            "n_silent_episodes": sum(ep["burst_faulty"] == 0 for ep in episodes),
            "label_stats": payload["label_stats"],
            "arms": {arm: {m: s[m] for m in METRICS} for arm, s in payload["summaries"].items()},
            "forfeiture": payload["forfeiture"],
        })
    arms = list(per_run[0]["arms"])
    keys = list(per_run[0]["forfeiture"])
    for r, config in zip(per_run, configs):
        if list(r["arms"]) != arms or list(r["forfeiture"]) != keys:
            raise ValueError(f"{r['run']} has different detectors from {per_run[0]['run']}")
        if config != configs[0]:
            raise ValueError(f"{r['run']} was scored with a different config from {per_run[0]['run']}")
    comparison = {
        "per_run": per_run,
        "aggregate": {
            "arms": {arm: {m: describe([r["arms"][arm][m] for r in per_run]) for m in METRICS} for arm in arms},
            "forfeiture": {k: describe([r["forfeiture"][k] for r in per_run]) for k in keys},
        },
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "comparison.json").write_text(json.dumps(comparison, indent=2), encoding="utf-8")
    (out_dir / "comparison.md").write_text(_render(comparison, arms, keys), encoding="utf-8")
    return comparison


def _render(comparison: Dict[str, Any], arms: List[str], keys: List[str]) -> str:
    lines = [
        f"# Evaluation runs ({len(comparison['per_run'])})",
        "",
        "| Run | Injections per category | Fault episodes (silent) | Windows (fault windows) | "
        + " | ".join([f"F1 {a}" for a in arms] + [f"Forfeiture {k}" for k in keys])
        + " |",
        "|---|" + "---:|" * (3 + len(arms) + len(keys)),
    ]
    for r in comparison["per_run"]:
        ls = r["label_stats"]
        cells = [str(r["injections_per_category"]), f"{r['n_fault_episodes']} ({r['n_silent_episodes']})",
                 f"{int(ls['n'])} ({int(ls['support_pos'])})"]
        cells += [_fmt(r["arms"][a]["f1"]) for a in arms] + [_fmt(r["forfeiture"][k]) for k in keys]
        lines.append(f"| {r['run']} | " + " | ".join(cells) + " |")

    def table(first_column: str, rows: Dict[str, Dict[str, Any]]) -> List[str]:
        out = [f"| {first_column} | mean | std | min | max | n | undefined |", "|---|---:|---:|---:|---:|---:|---:|"]
        for name, s in rows.items():
            out.append(f"| {name} | {_fmt(s['mean'])} | {_fmt(s['std'])} | {_fmt(s['min'])} | "
                       f"{_fmt(s['max'])} | {s['n']} | {s['n_undefined']} |")
        return out + [""]

    lines += ["", "## Over the runs", ""]
    for arm in arms:
        lines += [f"### {arm}", ""] + table("Metric", comparison["aggregate"]["arms"][arm])
    lines += ["### Forfeiture (baseline minus source-free)", ""] + table("Key", comparison["aggregate"]["forfeiture"])
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    out_dir = Path(args[0])
    compare_runs(out_dir, [Path(p) for p in args[1:]])
    print(f"Wrote {out_dir / 'comparison.json'} and {out_dir / 'comparison.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
