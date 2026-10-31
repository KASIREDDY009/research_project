"""Sanity checks that reject degenerate evaluation label sets."""

from __future__ import annotations

from typing import Dict

import numpy as np


class EvalLabelSanityError(ValueError):
    """Raised when the scored label set is degenerate (no usable negatives/positives)."""


def window_label_stats(y_true: np.ndarray) -> Dict[str, float]:
    y = np.asarray(y_true).astype(int)
    n = int(len(y))
    support_pos = int(y.sum())
    support_neg = n - support_pos
    pos_rate = float(support_pos / n) if n else float("nan")
    return {
        "n": float(n),
        "support_pos": float(support_pos),
        "support_neg": float(support_neg),
        "pos_rate": pos_rate,
    }


def assert_eval_label_sanity(
    y_true: np.ndarray,
    *,
    max_pos_rate: float,
    min_pos_rate: float,
    min_negatives: int,
    min_positives: int,
    context: str = "eval",
) -> Dict[str, float]:
    """Raise when labels lack a class or the positive share is outside the allowed range."""
    stats = window_label_stats(y_true)
    n = int(stats["n"])
    support_neg = int(stats["support_neg"])
    support_pos = int(stats["support_pos"])
    pos_rate = float(stats["pos_rate"])

    problems = []
    if n == 0:
        problems.append("empty scored set")
    if support_neg < min_negatives:
        problems.append(f"support_neg={support_neg} < {min_negatives}")
    if support_pos < min_positives:
        problems.append(f"support_pos={support_pos} < {min_positives}")
    if pos_rate > max_pos_rate:
        problems.append(f"pos_rate={pos_rate:.3f} > max_pos_rate={max_pos_rate}")
    if pos_rate < min_pos_rate and support_pos >= min_positives:
        problems.append(f"pos_rate={pos_rate:.3f} < min_pos_rate={min_pos_rate}")

    if problems:
        raise EvalLabelSanityError(
            f"Eval label sanity failed ({context}): {'; '.join(problems)}. "
            f"stats={stats}."
        )
    return stats
