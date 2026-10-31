"""Detector interface and shared feature helpers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import scipy.sparse as sp

from sflad.data.schema import LogEvent
from sflad.parsing.template_parser import assign_templates, build_parser

UNK_TOKEN = "__UNK__"

KEYWORD_GROUPS = {
    "err": ["error", "exception"],
    "permission": ["accessdenied", "unauthorized", "forbidden"],
    "config": ["resourcenotfound", "configerror", "missing environment", "invalidparameter"],
    "timeout": ["timed out", "timeout"],
    "resource": ["outofmemory", "throttling", "concurrency"],
}


@dataclass
class DetectionResult:
    name: str
    y_true: np.ndarray
    y_pred: np.ndarray
    scores: Optional[np.ndarray] = None
    event_indices: Optional[np.ndarray] = None
    meta: Optional[dict] = None


def build_template_vocab(template_ids: Sequence[str]) -> Dict[str, int]:
    uniq = sorted(set(template_ids))
    vocab = {t: i for i, t in enumerate(uniq)}
    if UNK_TOKEN not in vocab:
        vocab[UNK_TOKEN] = len(vocab)
    return vocab


def map_template_ids(template_ids: Sequence[str], vocab: Dict[str, int]) -> List[str]:
    """Map template IDs unseen at fit time to UNK, so the feature width stays fixed."""
    return [tid if tid in vocab else UNK_TOKEN for tid in template_ids]


def window_template_shares(
    template_ids: Sequence[str],
    vocab: Dict[str, int],
    window_size: int,
    step_size: int,
) -> Tuple[sp.csr_matrix, np.ndarray]:
    """Share of each known template in every sliding window, as a sparse matrix.

    Returns (X, end_indices) where end_indices[i] is the inclusive end event index; a window
    holds at most window_size templates, so the matrix stays small for any vocabulary.
    """
    ends = window_end_indices(len(template_ids), window_size, step_size)
    rows: List[int] = []
    cols: List[int] = []
    shares: List[float] = []
    for row, end in enumerate(ends):
        counts = Counter(vocab[t] for t in template_ids[max(0, end - window_size + 1) : end + 1] if t in vocab)
        total = sum(counts.values())
        for col, count in counts.items():
            rows.append(row)
            cols.append(col)
            shares.append(count / total)
    return sp.csr_matrix((shares, (rows, cols)), shape=(len(ends), len(vocab)), dtype=np.float64), ends


def window_features(
    template_ids: Sequence[str],
    vocab: Dict[str, int],
    window_size: int,
    step_size: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """Bag-of-templates features per sliding window, dense."""
    X, ends = window_template_shares(template_ids, vocab, window_size, step_size)
    return X.toarray(), ends


def window_labels(events: Sequence[LogEvent], end_indices: np.ndarray, window_size: int) -> np.ndarray:
    """A window is anomalous if any event in the window is anomalous."""
    labels = []
    for end in end_indices:
        start = max(0, int(end) - window_size + 1)
        anom = any(events[i].is_anomaly for i in range(start, int(end) + 1))
        labels.append(1 if anom else 0)
    return np.asarray(labels, dtype=int)


class ContaminatedTrainingWindowError(ValueError):
    """The training split contains injected anomalies: the clean window was not certified."""


def certified_train_events(events: Sequence[LogEvent]) -> List[LogEvent]:
    """Return the chronological training split; raise when it is missing or contains anomalies.

    Labels are only checked here; they never filter data.
    """
    train = [e for e in events if e.split == "train"]
    if not train:
        raise ValueError(
            "No events with split == 'train': a certified-clean training window is required."
        )
    n_bad = sum(1 for e in train if e.is_anomaly)
    if n_bad:
        raise ContaminatedTrainingWindowError(
            f"The training window holds {n_bad} line(s) of failed calls; it must hold none."
        )
    return train


def training_and_calibration_events(
    events: Sequence[LogEvent], calib_share: float, train_share: float = 1.0
) -> Tuple[List[LogEvent], List[LogEvent]]:
    """Split the certified fault-free training window in time: the earlier lines train a detector, the
    later calib_share of the lines set its alarm threshold. train_share keeps only the earliest share
    of the training part (the clean-data amount check); the calibration part never changes."""
    if not 0.0 < calib_share < 1.0:
        raise ValueError(f"calib_share must be between 0 and 1, got {calib_share}")
    if not 0.0 < train_share <= 1.0:
        raise ValueError(f"train_share must be in (0, 1], got {train_share}")
    clean = certified_train_events(events)
    cut = int(len(clean) * (1.0 - calib_share))
    fit, calib = clean[:cut], clean[cut:]
    return fit[: int(len(fit) * train_share)], calib


def alarm_threshold(calib_scores: np.ndarray, calib_fpr: float) -> float:
    """Smallest threshold at which at most calib_fpr of the calibration windows alarm (score >= threshold)."""
    ranked = np.sort(np.asarray(calib_scores, dtype=np.float64))[::-1]
    if not len(ranked):
        raise ValueError("the calibration part holds no window")
    return float(np.nextafter(ranked[int(calib_fpr * len(ranked))], np.inf))


def window_end_indices(n: int, window_size: int, step_size: int) -> np.ndarray:
    """Inclusive end index of every sliding window (the same grid as window_features)."""
    if n < window_size:
        return np.array([max(n - 1, 0)], dtype=int)
    return np.arange(window_size - 1, n, step_size, dtype=int)


def prepare_events(events: Sequence[LogEvent]) -> Tuple[List[str], List[str], object]:
    parser = build_parser()
    tids, templates = assign_templates([e.message for e in events], parser=parser)
    return tids, templates, parser


def lexical_window_features(
    events: Sequence[LogEvent],
    end_indices: np.ndarray,
    window_size: int,
) -> np.ndarray:
    """Domain-shared lexical features (transfer between the source and target systems)."""
    rows = []
    for end in end_indices:
        start = max(0, int(end) - window_size + 1)
        chunk = events[start : int(end) + 1]
        msgs = [e.message.lower() for e in chunk]
        n = max(len(msgs), 1)
        error_levels = sum(1 for e in chunk if e.level.upper() == "ERROR") / n
        feats = [error_levels]
        for keys in KEYWORD_GROUPS.values():
            hits = sum(1 for m in msgs if any(k in m for k in keys)) / n
            feats.append(hits)
        rows.append(feats)
    return np.asarray(rows, dtype=np.float64)


def combined_features(
    template_ids: Sequence[str],
    events: Sequence[LogEvent],
    vocab: Dict[str, int],
    window_size: int,
    step_size: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """Bag-of-templates concatenated with lexical features."""
    X_t, ends = window_features(template_ids, vocab, window_size, step_size)
    X_l = lexical_window_features(events, ends, window_size)
    return np.hstack([X_t, X_l]), ends


class BaseDetector(ABC):
    name: str = "base"

    @abstractmethod
    def fit(self, events: Sequence[LogEvent], **kwargs) -> "BaseDetector":
        ...

    @abstractmethod
    def predict(self, events: Sequence[LogEvent], **kwargs) -> DetectionResult:
        ...
