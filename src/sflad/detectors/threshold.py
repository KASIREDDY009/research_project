"""Keyword threshold alarms: a window alarms when enough of its lines hold an error keyword."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from sflad.data.schema import LogEvent
from sflad.detectors.base import BaseDetector, DetectionResult, window_end_indices, window_labels


class ThresholdDetector(BaseDetector):
    name = "threshold"

    def __init__(
        self,
        error_keywords: Sequence[str],
        window_size: int = 20,
        step_size: int = 20,
        min_keyword_count: int = 2,
    ) -> None:
        if not error_keywords:
            raise ValueError("the threshold detector needs at least one error keyword")
        self.keywords = list(error_keywords)
        self.window_size = int(window_size)
        self.step_size = int(step_size)
        self.min_keyword_count = int(min_keyword_count)

    def _is_error(self, message: str) -> bool:
        lower = message.lower()
        return any(k.lower() in lower for k in self.keywords)

    def fit(self, events: Sequence[LogEvent], **kwargs) -> "ThresholdDetector":
        return self

    def predict(self, events: Sequence[LogEvent], **kwargs) -> DetectionResult:
        eval_events = [e for e in events if e.split == "eval"]
        if not eval_events:
            raise ValueError("no evaluation events (split == 'eval') to score")
        flags = np.array([self._is_error(e.message) for e in eval_events], dtype=int)
        ends = window_end_indices(len(flags), self.window_size, self.step_size)
        hits = np.array([flags[max(0, end - self.window_size + 1) : end + 1].sum() for end in ends])
        y_pred = (hits >= self.min_keyword_count).astype(int)
        return DetectionResult(
            name=self.name,
            y_true=window_labels(eval_events, ends, self.window_size),
            y_pred=y_pred,
            scores=hits.astype(float),
            event_indices=ends,
            meta={"min_keyword_count": self.min_keyword_count, "n_windows": int(len(y_pred))},
        )
