"""Source-free one-class detectors: no labelled source is used.

SourceFreeDetector trains on the training part of the application's certified fault-free window and
sets its alarm threshold on the separate, later calibration part. It combines an Isolation Forest with
a novelty gate; either part can be switched off, giving the Isolation Forest alone or the gate alone.

SourceFeatureForest is the same detector on the labelled-source baseline's feature space (the source
corpus's template vocabulary plus the six lexical features). It reads the source corpus only for its
templates, never its labels, so it differs from the baseline in training data and labels but not in
features.
"""

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np
from sklearn.ensemble import IsolationForest

from sflad.data.schema import LogEvent
from sflad.detectors.base import (
    BaseDetector,
    DetectionResult,
    alarm_threshold,
    build_template_vocab,
    combined_features,
    map_template_ids,
    prepare_events,
    training_and_calibration_events,
    window_labels,
)
from sflad.detectors.transfer import source_space_features
from sflad.parsing.template_parser import assign_templates


def _forest(n_estimators: int, random_state: int) -> IsolationForest:
    return IsolationForest(n_estimators=n_estimators, random_state=random_state, n_jobs=1)


def _eval_events(events: Sequence[LogEvent]) -> list:
    eval_events = [e for e in events if e.split == "eval"]
    if not eval_events:
        raise ValueError("no evaluation events (split == 'eval') to score")
    return eval_events


class SourceFreeDetector(BaseDetector):
    name = "source_free"

    def __init__(
        self,
        calib_fpr: float = 0.01,
        calib_share: float = 0.5,
        train_share: float = 1.0,
        n_estimators: int = 100,
        window_size: int = 20,
        step_size: int = 20,
        random_state: int = 42,
        use_forest: bool = True,
        use_novelty_gate: bool = True,
    ) -> None:
        if not (use_forest or use_novelty_gate):
            raise ValueError("the detector needs the Isolation Forest, the novelty gate or both")
        self.calib_fpr = float(calib_fpr)
        self.calib_share = float(calib_share)
        self.train_share = float(train_share)
        self.n_estimators = n_estimators
        self.window_size = window_size
        self.step_size = step_size
        self.random_state = random_state
        self.use_forest = bool(use_forest)
        # The gate flags a window with a positive value on a dimension that is zero across the training part.
        self.use_novelty_gate = bool(use_novelty_gate)
        self.model: Optional[IsolationForest] = None
        self.vocab = None
        self._parser = None
        self._train_max: Optional[np.ndarray] = None
        self.alarm_threshold: Optional[float] = None
        self.n_train_windows: Optional[int] = None
        self.n_calib_windows: Optional[int] = None

    def _space(self, fit_events: Sequence[LogEvent], **kwargs) -> None:
        """The template parser and vocabulary of the feature space: the training part's own templates."""
        tids, _, self._parser = prepare_events(fit_events)
        self.vocab = build_template_vocab(tids)

    def _features(self, events: Sequence[LogEvent]):
        tids, _ = assign_templates([e.message for e in events], parser=self._parser)
        return combined_features(map_template_ids(tids, self.vocab), events, self.vocab,
                                 self.window_size, self.step_size)

    def _novel(self, X: np.ndarray) -> np.ndarray:
        eps = 1e-12
        dims = np.where(self._train_max <= eps)[0]
        return (X[:, dims] > (self._train_max[dims] + eps)).any(axis=1)

    def fit(self, events: Sequence[LogEvent], **kwargs) -> "SourceFreeDetector":
        """Train on the training part; kwargs reach _space (SourceFeatureForest takes source_events)."""
        fit_events, calib_events = training_and_calibration_events(events, self.calib_share, self.train_share)
        self._space(fit_events, **kwargs)
        X, _ = self._features(fit_events)
        self.n_train_windows = int(X.shape[0])
        self._train_max = np.asarray(X, dtype=np.float64).max(axis=0)
        X_cal, _ = self._features(calib_events)
        self.n_calib_windows = int(X_cal.shape[0])
        if self.use_forest:
            self.model = _forest(self.n_estimators, self.random_state).fit(X)
            self.alarm_threshold = alarm_threshold(-self.model.decision_function(X_cal), self.calib_fpr)
        return self

    def predict(self, events: Sequence[LogEvent], **kwargs) -> DetectionResult:
        if self.vocab is None:
            raise RuntimeError("SourceFreeDetector must be fit before predict")
        eval_events = _eval_events(events)
        X, ends = self._features(eval_events)
        y_pred = np.zeros(X.shape[0], dtype=int)
        scores = np.zeros(X.shape[0])
        if self.use_forest:
            scores = -self.model.decision_function(X)
            y_pred = (scores >= self.alarm_threshold).astype(int)
        n_novel: Optional[int] = None
        if self.use_novelty_gate:
            novel = self._novel(X)
            n_novel = int(novel.sum())
            y_pred = np.where(novel, 1, y_pred)
            # A positive margin keeps the score ranking consistent with the gate.
            scores = scores + novel.astype(float)
        return DetectionResult(
            name=self.name,
            y_true=window_labels(eval_events, ends, self.window_size),
            y_pred=y_pred,
            scores=scores,
            event_indices=ends,
            meta={
                "algorithm": "isolation_forest" if self.use_forest else "novelty_gate",
                "use_forest": self.use_forest,
                "use_novelty_gate": self.use_novelty_gate,
                "decision_threshold": self.alarm_threshold,
                "calib_fpr": self.calib_fpr,
                "n_train_windows": self.n_train_windows,
                "n_calib_windows": self.n_calib_windows,
                "n_novelty_gate_windows": n_novel,
                "n_windows": int(len(y_pred)),
            },
        )


class SourceFeatureForest(SourceFreeDetector):
    """The source-free detector (Isolation Forest with novelty gate) on the labelled-source baseline's
    feature space; the source corpus gives only its template vocabulary, never its labels."""

    name = "source_free_source_features"

    def _space(self, fit_events: Sequence[LogEvent], source_events=None, **kwargs) -> None:
        if source_events is None:
            raise ValueError("SourceFeatureForest needs source_events for the source template vocabulary")
        tids, _, self._parser = prepare_events(source_events)
        self.vocab = build_template_vocab(tids)

    def _features(self, events: Sequence[LogEvent]):
        X, ends = source_space_features(events, self._parser, self.vocab, self.window_size, self.step_size)
        return X.toarray(), ends

    def predict(self, events: Sequence[LogEvent], **kwargs) -> DetectionResult:
        result = super().predict(events, **kwargs)
        result.meta["feature_space"] = "labelled-source baseline (source templates and lexical features)"
        return result
