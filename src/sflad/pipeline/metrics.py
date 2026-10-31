"""Precision, recall, F1, MCC, false-alarm rate, fault-segment detection and delay, and window fault categories.

A ratio with a zero denominator is returned as NaN.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List

import numpy as np

from sflad.data.schema import normalize_fault_category

def precision_recall_f1(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    y_true = np.asarray(y_true).astype(int)
    y_pred = np.asarray(y_pred).astype(int)
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())
    nan = float("nan")
    precision = tp / (tp + fp) if (tp + fp) else nan
    recall = tp / (tp + fn) if (tp + fn) else nan
    f1 = 2 * tp / (2 * tp + fp + fn) if (tp + fn) else nan
    denom = float((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)) ** 0.5
    mcc = (tp * tn - fp * fn) / denom if denom else nan
    return {
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "mcc": float(mcc),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "support_pos": int(y_true.sum()),
        "n": int(len(y_true)),
    }


def false_alarm_rate(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """FPR = FP / (FP + TN) on negative windows."""
    y_true = np.asarray(y_true).astype(int)
    y_pred = np.asarray(y_pred).astype(int)
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())
    return float(fp / (fp + tn)) if (fp + tn) else float("nan")


def segment_hits(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """One boolean per fault segment (a run of consecutive fault windows): any alarm inside it."""
    y_true = np.asarray(y_true).astype(int)
    y_pred = np.asarray(y_pred).astype(int)
    hits = []
    i, n = 0, len(y_true)
    while i < n:
        if y_true[i] != 1:
            i += 1
            continue
        start = i
        while i < n and y_true[i] == 1:
            i += 1
        hits.append(bool(y_pred[start:i].any()))
    return np.asarray(hits, dtype=bool)


def segment_delays(y_true: np.ndarray, y_pred: np.ndarray, end_ms: np.ndarray) -> List[Dict[str, float]]:
    """Per fault segment: windows and seconds from the end of its first window to the end of its first
    alarmed window (0 when the first window alarms); both are NaN when no window of the segment alarms."""
    y_true = np.asarray(y_true).astype(int)
    y_pred = np.asarray(y_pred).astype(int)
    end_ms = np.asarray(end_ms, dtype=float)
    out = []
    i, n = 0, len(y_true)
    while i < n:
        if y_true[i] != 1:
            i += 1
            continue
        start = i
        while i < n and y_true[i] == 1:
            i += 1
        alarms = np.flatnonzero(y_pred[start:i])
        if alarms.size:
            first = start + int(alarms[0])
            out.append({"windows": float(first - start), "seconds": (end_ms[first] - end_ms[start]) / 1000.0})
        else:
            out.append({"windows": float("nan"), "seconds": float("nan")})
    return out


def delay_summary(delays: List[Dict[str, float]]) -> Dict[str, Any]:
    """Mean and median delay over the detected segments, with how many segments were detected."""
    w = np.array([d["windows"] for d in delays], dtype=float)
    sec = np.array([d["seconds"] for d in delays], dtype=float)
    hit = ~np.isnan(w)
    return {
        "n_segments": int(len(w)),
        "n_detected_segments": int(hit.sum()),
        "mean_delay_windows": float(w[hit].mean()) if hit.any() else None,
        "median_delay_seconds": float(np.median(sec[hit])) if hit.any() else None,
        "mean_delay_seconds": float(sec[hit].mean()) if hit.any() else None,
    }


def summarise_result(y_true, y_pred) -> Dict[str, float]:
    m = precision_recall_f1(y_true, y_pred)
    m["false_alarm_rate"] = false_alarm_rate(y_true, y_pred)
    return m


# The five injected fault categories, in their canonical order.
FAULT_CATEGORIES = ("permission", "config", "timeout", "resource", "latency")
_WINDOW_CATEGORY_ORDER = FAULT_CATEGORIES + ("unattributed",)


def window_fault_categories(
    events,
    end_indices: np.ndarray,
    window_size: int,
) -> np.ndarray:
    """Assign each sliding window a fault category string.

    A window without anomalous lines is ``none``; otherwise it takes the majority category of its
    anomalous lines, ties broken by the canonical order.
    """
    cats: list[str] = []
    for end in end_indices:
        start = max(0, int(end) - window_size + 1)
        anom_cats = []
        for i in range(start, int(end) + 1):
            ev = events[i]
            if not ev.is_anomaly:
                continue
            cat = normalize_fault_category(ev.fault_category)
            if cat != "none":
                anom_cats.append(cat)
        if not anom_cats:
            cats.append("none")
            continue
        counts = Counter(anom_cats)
        best = max(counts.keys(), key=lambda c: (counts[c], -_WINDOW_CATEGORY_ORDER.index(c)))
        cats.append(best)
    return np.asarray(cats, dtype=object)
