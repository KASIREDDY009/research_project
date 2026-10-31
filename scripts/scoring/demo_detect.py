#!/usr/bin/env python3
"""Score logs with a saved detector: a run's labelled events, or an application's recent CloudWatch logs.

  python scripts/scoring/demo_detect.py results/runs/TAG/orders/processed/models/source_free.joblib \\
      --events results/runs/TAG/orders/raw/events.jsonl
  python scripts/scoring/demo_detect.py results/runs/TAG/orders/processed/models/transfer.joblib --app orders --minutes 10

Every window the model alarms on is listed with its warning and error lines; with labelled events
the precision, recall, F1 and MCC of the saved model on those events are printed too.
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import replace
from pathlib import Path

import joblib
import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from sflad.aws.evaluation_run import terraform_apps  # noqa: E402
from sflad.aws.collect_logs import export_events, parse_line  # noqa: E402
from sflad.data.schema import LogEvent  # noqa: E402
from sflad.data.event_io import events_from_jsonl  # noqa: E402
from sflad.pipeline.metrics import precision_recall_f1  # noqa: E402


def cloudwatch_events(app_name: str, minutes: int) -> list[LogEvent]:
    cfg = yaml.safe_load((ROOT / "configs" / "aws.yaml").read_text())
    app = terraform_apps(ROOT / cfg["terraform_dir"])[app_name]
    now = int(time.time() * 1000)
    events = []
    for raw in sorted(export_events(app["log_group"], now - minutes * 60_000, now, region=cfg["region"]),
                      key=lambda e: e["timestamp"]):
        level, rid, text = parse_line(raw["message"])
        if text.strip():
            events.append(LogEvent(timestamp_ms=int(raw["timestamp"]), message=text, log_group=app["log_group"],
                                   log_stream=raw.get("logStreamName", ""), request_id=rid,
                                   level=level, split="eval"))
    return events


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("model", type=Path)
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("--events", type=Path, help="labelled events.jsonl of an evaluation run")
    source.add_argument("--app", choices=["orders", "bookings"], help="read the deployed application's logs")
    p.add_argument("--minutes", type=int, default=10)
    p.add_argument("--show", type=int, default=10, help="alarmed windows to list")
    a = p.parse_args(argv)

    detector = joblib.load(a.model)
    if a.events:
        events = [replace(e, split="eval") for e in events_from_jsonl(a.events)]
    else:
        events = cloudwatch_events(a.app, a.minutes)
    if not events:
        print("no log lines to score")
        return 0
    result = detector.predict(events)
    alarms = np.flatnonzero(result.y_pred)
    print(f"{a.model.stem}: {len(result.y_pred)} windows of {detector.window_size} lines, {len(alarms)} alarms")
    if a.events:
        m = precision_recall_f1(result.y_true, result.y_pred)
        print(f"precision {m['precision']:.3f}  recall {m['recall']:.3f}  F1 {m['f1']:.3f}  MCC {m['mcc']:.3f}")
    for w in alarms[: a.show]:
        end = int(result.event_indices[w])
        start = max(0, end - detector.window_size + 1)
        print(f"-- alarm on lines {start}-{end}, score {float(result.scores[w]):.3f}")
        for e in events[start : end + 1]:
            if e.level in ("ERROR", "WARNING") or "Status:" in e.message:
                print(f"   [{e.level}] {e.message[:160]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
