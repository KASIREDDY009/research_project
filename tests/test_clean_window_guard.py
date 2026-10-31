from __future__ import annotations

from dataclasses import replace

import pytest

from sflad.data.schema import LogEvent
from sflad.detectors.base import (
    ContaminatedTrainingWindowError,
    certified_train_events,
    window_end_indices,
)
from sflad.detectors.source_free import SourceFreeDetector


def _events(n: int = 40, split: str = "train"):
    return [LogEvent(timestamp_ms=i, message=f"request {i} ok", split=split) for i in range(n)]


def test_certified_train_events_returns_only_train_split():
    events = _events(10) + _events(5, split="eval")
    assert len(certified_train_events(events)) == 10


def test_contaminated_window_fails_loudly():
    events = _events(10)
    events[3] = replace(events[3], is_anomaly=True)
    with pytest.raises(ContaminatedTrainingWindowError):
        certified_train_events(events)


def test_missing_train_split_fails_loudly():
    with pytest.raises(ValueError):
        certified_train_events(_events(10, split="eval"))


def test_source_free_detector_uses_the_guard():
    events = _events(40)
    events[7] = replace(events[7], is_anomaly=True)
    det = SourceFreeDetector(window_size=5, step_size=5)
    with pytest.raises(ContaminatedTrainingWindowError):
        det.fit(events)


def test_window_end_indices_matches_window_features_grid():
    assert window_end_indices(3, 5, 5).tolist() == [2]
    assert window_end_indices(12, 5, 5).tolist() == [4, 9]
