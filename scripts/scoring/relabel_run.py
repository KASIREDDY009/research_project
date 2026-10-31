#!/usr/bin/env python3
"""Rebuild a run's events.jsonl and export.json from its raw files, without AWS."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from sflad.aws.collect_logs import label_events  # noqa: E402
from sflad.aws.evaluation_run import summarise_export  # noqa: E402


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.open()]


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: relabel_run.py RAW_DIR OUT_DIR")
    raw, out = Path(sys.argv[1]), Path(sys.argv[2])
    meta = json.loads((raw / "run.json").read_text())
    exported = read_jsonl(raw / "cloudwatch_events.jsonl")
    records = read_jsonl(raw / "invocations.jsonl")
    episodes = read_jsonl(raw / "episodes.jsonl")
    events = label_events(exported, records, meta["deployed"]["log_group"], meta["times"], episodes,
                          meta["slow_limit_ms"])
    out.mkdir(parents=True, exist_ok=True)
    with (out / "events.jsonl").open("w") as f:
        for ev in events:
            f.write(json.dumps(ev.to_dict()) + "\n")
    summary = summarise_export(records, episodes, events, len(exported), meta["slow_limit_ms"])
    (out / "export.json").write_text(json.dumps(summary, indent=2))
    print(f"{len(events)} labelled lines -> {out.name}/events.jsonl and export.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
