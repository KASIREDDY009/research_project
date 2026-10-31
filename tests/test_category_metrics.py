"""The fault category of each window."""

from __future__ import annotations

import numpy as np

from sflad.data.schema import LogEvent
from sflad.pipeline.metrics import window_fault_categories


def _ev(i: int, *, anom: bool = False, cat: str = "none", split: str = "eval") -> LogEvent:
    msg = "INFO ok"
    level = "INFO"
    if anom and cat == "permission":
        msg, level = "ERROR AccessDenied on table", "ERROR"
    elif anom and cat == "config":
        msg, level = "ERROR ConfigError missing env", "ERROR"
    elif anom and cat == "timeout":
        msg, level = "ERROR Timed out calling dependency", "ERROR"
    elif anom and cat == "resource":
        msg, level = "ERROR OutOfMemory at heap", "ERROR"
    return LogEvent(
        timestamp_ms=1_700_000_000_000 + i * 1000,
        message=msg,
        is_anomaly=anom,
        fault_category=cat,
        split=split,
        level=level,
    )


def _tiny_eval_events():
    """Clean → permission burst → clean → config burst → clean."""
    events = []
    for i in range(50):
        if 10 <= i <= 12:
            events.append(_ev(i, anom=True, cat="permission"))
        elif 30 <= i <= 32:
            events.append(_ev(i, anom=True, cat="config"))
        else:
            events.append(_ev(i))
    return events


def test_window_fault_categories_majority():
    events = _tiny_eval_events()
    ends = np.asarray([14, 20, 34, 45], dtype=int)
    cats = window_fault_categories(events, ends, window_size=5)
    assert list(cats) == ["permission", "none", "config", "none"]


def test_every_injected_category_is_a_known_window_category():
    import numpy as np

    from sflad.data.schema import LogEvent, normalize_fault_category
    from sflad.pipeline.metrics import FAULT_CATEGORIES, window_fault_categories

    assert [normalize_fault_category(c) for c in FAULT_CATEGORIES] == list(FAULT_CATEGORIES)
    events = [LogEvent(timestamp_ms=i, message="m", is_anomaly=True, fault_category="latency", split="eval") for i in range(4)]
    assert list(window_fault_categories(events, np.array([3]), 4)) == ["latency"]
