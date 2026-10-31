"""Loaders for full LogHub corpora: BGL, HDFS v1 and OpenStack.

Each loader streams at most ``max_lines`` lines in file order and returns LogEvents with line-level
labels. The message is the line's content field, and severity comes from the line's own level field.
"""

from __future__ import annotations

import csv
import re
from dataclasses import replace
from pathlib import Path
from typing import Iterator, List, Optional, Sequence

from sflad.data.schema import LogEvent

_BLOCK = re.compile(r"blk_-?\d+")
_UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
_ERROR_LEVELS = {"FATAL", "SEVERE", "FAILURE", "ERROR", "ERR", "CRITICAL", "CRIT", "ALERT", "EMERG"}
_WARN_LEVELS = {"WARN", "WARNING"}
_INFO_LEVELS = {"INFO", "NOTICE", "DEBUG", "TRACE"}
# A BGL line's severity is the first severity token after its header. A few lines in the full
# corpus drop a header field (for example a missing NodeRepeat), which moves the token left.
_BGL_LINE = re.compile(r"^(\S+)(?:\s+\S+){5,11}?\s+(INFO|WARNING|SEVERE|ERROR|FATAL|FAILURE)(?:\s+(.*))?$")


def _level(token: str) -> str:
    """Map a line's own severity token; a token that is no severity gives "UNKNOWN"."""
    t = token.upper()
    if t in _ERROR_LEVELS:
        return "ERROR"
    if t in _WARN_LEVELS:
        return "WARNING"
    if t in _INFO_LEVELS:
        return "INFO"
    return "UNKNOWN"


def _lines(path: Path, max_lines: Optional[int]) -> Iterator[str]:
    with open(path, encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f):
            if max_lines is not None and i >= max_lines:
                return
            line = line.rstrip("\n")
            if line.strip():
                yield line


def load_bgl(path: Path, max_lines: Optional[int] = None, split: str = "source") -> List[LogEvent]:
    """BGL: ``<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>``.

    The label is '-' for normal lines, otherwise the alert category, kept in ``meta["loghub_label"]``;
    ``fault_category`` stays "none".
    """
    events = []
    for i, line in enumerate(_lines(Path(path), max_lines)):
        found = _BGL_LINE.match(line)
        label = line.split(None, 1)[0]
        if found:
            level, message = _level(found.group(2)), found.group(3) or ""
        else:
            parts = line.split(None, 9)
            level, message = "UNKNOWN", parts[9] if len(parts) > 9 else ""
        events.append(
            LogEvent(
                timestamp_ms=i,
                message=message,
                level=level,
                is_anomaly=label != "-",
                split=split,
                meta={"loghub": "BGL", "loghub_label": label},
            )
        )
    return events


def load_hdfs(
    log_path: Path,
    label_csv: Path,
    max_lines: Optional[int] = None,
    split: str = "eval",
    group_by_block: bool = False,
) -> List[LogEvent]:
    """HDFS v1: ``<Date> <Time> <Pid> <Level> <Component>: <Content>``.

    A line is anomalous if it mentions a block labelled 'Anomaly'. ``group_by_block=True`` orders the
    lines block by block (blocks in order of first appearance, a line with several blocks under its first).
    """
    anomalous = set()
    with open(label_csv, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["Label"].strip().lower() == "anomaly":
                anomalous.add(row["BlockId"].strip())
    events = []
    for i, line in enumerate(_lines(Path(log_path), max_lines)):
        parts = line.split(None, 5)
        events.append(
            LogEvent(
                timestamp_ms=i,
                message=parts[5] if len(parts) > 5 else "",
                level=_level(parts[3]) if len(parts) > 3 else "UNKNOWN",
                is_anomaly=bool(set(_BLOCK.findall(line)) & anomalous),
                split=split,
                meta={"loghub": "HDFS"},
            )
        )
    if not group_by_block:
        return events
    sessions: dict = {}
    for e in events:
        found = _BLOCK.search(e.message)
        sessions.setdefault(found.group(0) if found else "", []).append(e)
    ordered = [e for block_events in sessions.values() for e in block_events]
    return [replace(e, timestamp_ms=k) for k, e in enumerate(ordered)]


def load_openstack(
    log_paths: Sequence[Path],
    labels_path: Path,
    max_lines: Optional[int] = None,
    split: str = "eval",
    anomalous_files: Sequence[Path] = (),
) -> List[LogEvent]:
    """OpenStack: ``<Logrecord> <Date> <Time> <Pid> <Level> <Component> [<ADDR>] <Content>``.

    A line is anomalous if it mentions a VM instance listed in anomaly_labels.txt, or if it comes
    from one of ``anomalous_files``.
    """
    anomalous = set(_UUID.findall(Path(labels_path).read_text(encoding="utf-8", errors="replace")))
    whole_file = {Path(f).resolve() for f in anomalous_files}
    events: List[LogEvent] = []
    for path in log_paths:
        in_anomalous_file = Path(path).resolve() in whole_file
        for line in _lines(Path(path), None):
            if max_lines is not None and len(events) >= max_lines:
                return events
            parts = line.split(None, 6)
            rest = parts[6] if len(parts) > 6 else ""
            events.append(
                LogEvent(
                    timestamp_ms=len(events),
                    message=rest.split("] ", 1)[1] if rest.startswith("[") and "] " in rest else rest,
                    level=_level(parts[4]) if len(parts) > 4 else "UNKNOWN",
                    is_anomaly=in_anomalous_file or bool(set(_UUID.findall(line)) & anomalous),
                    split=split,
                    meta={"loghub": "OpenStack"},
                )
            )
    return events


def split_chronological(events: Sequence[LogEvent], train_frac: float = 0.5) -> List[LogEvent]:
    """First ``train_frac`` of events -> 'train' (used unlabelled); the rest -> 'eval'."""
    cut = int(len(events) * train_frac)
    return [replace(e, split="train" if k < cut else "eval") for k, e in enumerate(events)]
