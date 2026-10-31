"""Labelled-source baseline: a random forest trained on windows of a labelled source corpus.

Features are each window's share of every source template plus six lexical features (the share of
error-level lines and of error, permission, config, timeout and resource keywords). The alarm
threshold is the smallest at which at most ``calib_fpr`` of the windows of the calibration part (the
later part of the certified fault-free training window) alarm; meta reports ``threshold_can_alarm``.
"""

from __future__ import annotations

from typing import Optional, Sequence, Tuple

import numpy as np
import scipy.sparse as sp
from sklearn.ensemble import RandomForestClassifier

from sflad.data.schema import LogEvent
from sflad.detectors.base import (
    BaseDetector,
    DetectionResult,
    alarm_threshold,
    build_template_vocab,
    lexical_window_features,
    map_template_ids,
    prepare_events,
    training_and_calibration_events,
    window_labels,
    window_template_shares,
)
from sflad.parsing.template_parser import assign_templates


def source_space_features(events: Sequence[LogEvent], parser, vocab, window_size: int,
                          step_size: int) -> Tuple[sp.csr_matrix, np.ndarray]:
    """Windows in the source corpus's feature space: source-template shares and the six lexical features."""
    tids, _ = assign_templates([e.message for e in events], parser=parser)
    X_t, ends = window_template_shares(map_template_ids(tids, vocab), vocab, window_size, step_size)
    X_l = lexical_window_features(events, ends, window_size)
    return sp.hstack([X_t, sp.csr_matrix(X_l)], format="csr"), ends


def _require_two_classes(y: np.ndarray) -> np.ndarray:
    """The labelled source must contain both normal and anomalous windows."""
    if len(np.unique(y)) < 2:
        raise ValueError("the labelled source needs both normal and anomalous windows")
    return y


class TransferDetector(BaseDetector):
    name = "transfer"

    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int = 12,
        class_weight: Optional[str] = "balanced",
        window_size: int = 20,
        step_size: int = 20,
        random_state: int = 42,
        calib_fpr: float = 0.01,
        calib_share: float = 0.5,
    ) -> None:
        if not 0.0 <= calib_fpr < 1.0:
            raise ValueError(f"calib_fpr must be in [0, 1), got {calib_fpr}")
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.class_weight = class_weight
        self.window_size = window_size
        self.step_size = step_size
        self.random_state = random_state
        self.calib_fpr = float(calib_fpr)
        self.calib_share = float(calib_share)
        self.alarm_threshold: Optional[float] = None
        self.n_calib_windows: Optional[int] = None
        self.n_source_windows: Optional[int] = None
        self.model: Optional[RandomForestClassifier] = None
        self.vocab = None
        self._parser = None

    def _rf(self) -> RandomForestClassifier:
        return RandomForestClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            random_state=self.random_state,
            n_jobs=1,
            class_weight=self.class_weight,
        )


    def fit(
        self,
        events: Sequence[LogEvent],
        source_events: Optional[Sequence[LogEvent]] = None,
        **kwargs,
    ) -> "TransferDetector":
        if source_events is None:
            raise ValueError("TransferDetector requires source_events (a labelled source corpus).")
        _, calib = training_and_calibration_events(events, self.calib_share)
        tids, _, self._parser = prepare_events(source_events)
        self.vocab = build_template_vocab(tids)
        X, ends = self._features(source_events)
        y = _require_two_classes(window_labels(source_events, ends, self.window_size))
        self.model = self._rf().fit(X, y)
        self.n_source_windows = int(X.shape[0])
        self._calibrate_threshold(calib)
        return self

    def _positive_scores(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)[:, list(self.model.classes_).index(1)]

    def _features(self, events: Sequence[LogEvent]) -> Tuple[sp.csr_matrix, np.ndarray]:
        return source_space_features(events, self._parser, self.vocab, self.window_size, self.step_size)

    def _calibrate_threshold(self, calib_events: Sequence[LogEvent]) -> None:
        X, _ = self._features(calib_events)
        self.alarm_threshold = alarm_threshold(self._positive_scores(X), self.calib_fpr)
        self.n_calib_windows = int(X.shape[0])

    def predict(self, events: Sequence[LogEvent], **kwargs) -> DetectionResult:
        if self.model is None:
            raise RuntimeError("TransferDetector must be fit before predict")
        eval_events = [e for e in events if e.split == "eval"]
        if not eval_events:
            raise ValueError("no evaluation events (split == 'eval') to score")
        X, ends = self._features(eval_events)
        scores = self._positive_scores(X)
        y_pred = (scores >= self.alarm_threshold).astype(int)
        y_true = window_labels(eval_events, ends, self.window_size)
        return DetectionResult(
            name=self.name,
            y_true=y_true,
            y_pred=y_pred,
            scores=scores,
            event_indices=ends,
            meta={
                "algorithm": "random_forest",
                "n_source_windows": self.n_source_windows,
                "decision_threshold": self.alarm_threshold,
                "threshold_can_alarm": bool(self.alarm_threshold <= 1.0),
                "calib_fpr": self.calib_fpr,
                "n_calib_windows": self.n_calib_windows,
                "n_windows": int(len(y_pred)),
            },
        )
