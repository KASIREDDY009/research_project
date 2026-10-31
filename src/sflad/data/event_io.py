"""Read and write log events as JSON lines, one LogEvent per line."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Sequence

from sflad.data.schema import LogEvent


def events_to_jsonl(events: Sequence[LogEvent], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for ev in events:
            f.write(json.dumps(ev.to_dict(), ensure_ascii=False) + "\n")


def events_from_jsonl(path: Path) -> List[LogEvent]:
    events: List[LogEvent] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            events.append(LogEvent.from_dict(json.loads(line)))
    return events
