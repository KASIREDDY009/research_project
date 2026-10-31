"""Export an application's CloudWatch logs and label every line from the recorded invocations.

A line's request id ties it to one recorded invocation, and the invocation's observed outcome
(workload.faulty: failed, slow or without the expected content) is the line's label; log text never
decides a label.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Sequence, Tuple

from sflad.aws.clients import make_client
from sflad.aws.workload import faulty
from sflad.data.schema import LogEvent

# Lambda's Python runtime prints "[LEVEL]\t<timestamp>\t<request id>\t<text>" for application lines;
# platform lines (START, END, REPORT) name the request id; INIT lines carry none.
_RUNTIME_LINE = re.compile(r"^\[(?P<level>[A-Z]+)\]\t\S+\t(?P<rid>[0-9a-f-]{36})\t(?P<text>.*)$", re.S)
_PLATFORM_ID = re.compile(r"RequestId: ([0-9a-f-]{36})")


class IncompleteExportError(RuntimeError):
    """The export lacks the REPORT line of at least one recorded invocation."""


def export_events(log_group: str, start_ms: int, end_ms: int, region: Optional[str] = None) -> List[dict]:
    """Every event of the log group between the two times.

    FilterLogEvents can return an empty page while more events remain behind its nextToken, so
    the paginator follows the token until the service stops returning one.
    """
    paginator = make_client("logs", region=region).get_paginator("filter_log_events")
    events: List[dict] = []
    for page in paginator.paginate(logGroupName=log_group, startTime=int(start_ms), endTime=int(end_ms)):
        events.extend(page.get("events") or [])
    return events


def parse_line(message: str) -> Tuple[str, str, str]:
    """(level, request id, text) of one CloudWatch line; UNKNOWN level and "" id when absent."""
    message = message.rstrip("\n")
    runtime = _RUNTIME_LINE.match(message)
    if runtime:
        return runtime["level"], runtime["rid"], runtime["text"]
    platform = _PLATFORM_ID.search(message)
    return "UNKNOWN", platform.group(1) if platform else "", message


def phase_at(ts: int, times: Dict[str, int], episodes: Sequence[dict]) -> str:
    """The run phase at a timestamp, from the recorded phase boundaries and episode intervals."""
    if ts < times["train_end"]:
        return "train"
    if "control_start" in times and ts >= times["control_start"]:
        return "control"
    if any(ep["inject_ms"] <= ts <= ep["restored_ms"] for ep in episodes):
        return "fault"
    return "gap"


def label_events(raw: Sequence[dict], records: Sequence[dict], log_group: str, times: Dict[str, int],
                 episodes: Sequence[dict], slow_limit_ms: int) -> List[LogEvent]:
    """Chronological LogEvents labelled by the outcome of the invocation each line belongs to.

    An initialisation line takes the next request id in its log stream; a line left without one stays
    negative and is marked meta["orphan"]. Raises when a recorded invocation has no REPORT line or an
    exported request id was not recorded.
    """
    by_id = {r["request_id"]: r for r in records}
    rows = []
    for e in raw:
        level, rid, text = parse_line(e["message"])
        if text.strip():
            rows.append([int(e["timestamp"]), e.get("logStreamName", ""), level, rid, text])
    streams: Dict[str, list] = {}
    for row in rows:
        streams.setdefault(row[1], []).append(row)
    for stream_rows in streams.values():
        following = ""
        for row in reversed(stream_rows):
            if row[3]:
                following = row[3]
            else:
                row[3] = following

    unknown = {row[3] for row in rows if row[3] and row[3] not in by_id}
    if unknown:
        raise ValueError(f"{len(unknown)} request id(s) in the export were not recorded by the evaluation run")
    reported = {row[3] for row in rows if row[4].startswith("REPORT ")}
    missing = set(by_id) - reported
    if missing:
        raise IncompleteExportError(f"{len(missing)} recorded invocation(s) have no REPORT line in the export")

    events = []
    for ts, stream, level, rid, text in sorted(rows, key=lambda r: r[0]):
        rec = by_id.get(rid)
        phase = rec["phase"] if rec else phase_at(ts, times, episodes)
        anomalous = bool(rec) and faulty(rec, slow_limit_ms)
        events.append(
            LogEvent(
                timestamp_ms=ts,
                message=text,
                log_group=log_group,
                log_stream=stream,
                request_id=rid,
                level=level,
                is_anomaly=anomalous,
                fault_category=(rec.get("category") or "unattributed") if anomalous else "none",
                split="train" if phase == "train" else "eval",
                meta={"phase": phase, "episode": rec.get("episode") if rec else None,
                      "strength_ms": rec.get("strength_ms") if rec else None, "orphan": rec is None},
            )
        )
    return events
