from __future__ import annotations

from synthetic_data import synthetic_config

from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from synthetic_faults import FaultInjector
from synthetic_logs import SyntheticLogGenerator, generate_dataset
from sflad.detectors.base import ContaminatedTrainingWindowError
from sflad.detectors.transfer import TransferDetector
from sflad.pipeline.metrics import false_alarm_rate, precision_recall_f1
from sflad.pipeline.train_eval import events_from_jsonl

ROOT = Path(__file__).resolve().parents[1]


def _corpus(seed: int = 5):
    gen = SyntheticLogGenerator(seed=seed)
    target = FaultInjector(seed=seed).inject(
        gen.generate_target(200, train_frac=0.5),
        fault_rate=0.05,
        inject_after_frac=0.5,
        min_fault_gap_events=10,
        categories=["permission", "config", "timeout", "resource"],
        fault_burst_size=2,
    )
    source = gen.generate_source(200, anomaly_rate=0.1)
    return target, source


def _det(**kw):
    return TransferDetector(
        window_size=10, step_size=5, random_state=0, **kw
    )


def _clean_window(target):
    return [replace(e, split="eval") for e in target if e.split == "train"]


def test_fit_never_reads_target_labels():
    # Training-window labels are only certified (a flipped one raises, see below).
    target, source = _corpus()
    flipped = [replace(e, is_anomaly=not e.is_anomaly) if e.split == "eval" else e for e in target]
    a = _det().fit(target, source_events=source).predict(target)
    b = _det().fit(flipped, source_events=source).predict(flipped)
    assert np.array_equal(a.y_pred, b.y_pred)
    assert np.allclose(a.scores, b.scores)
    assert a.meta["decision_threshold"] == b.meta["decision_threshold"]


def test_the_baseline_records_its_source_and_clean_window_calibration():
    target, source = _corpus()
    res = _det().fit(target, source_events=source).predict(target)
    assert res.meta["n_source_windows"] > 0
    assert res.meta["n_calib_windows"] > 0


def test_clean_window_threshold_bounds_alarms_on_the_clean_window():
    target, source = _corpus()
    det = _det(calib_fpr=0.1).fit(target, source_events=source)
    clean = det.predict(_clean_window(target))
    assert clean.y_pred.mean() <= 0.1


def test_clean_window_threshold_needs_a_certified_clean_window():
    target, source = _corpus()
    evals = [e for e in target if e.split == "eval"]
    with pytest.raises(ValueError, match="training window"):
        _det().fit(evals, source_events=source)
    dirty = [replace(e, is_anomaly=True) if e.split == "train" else e for e in target]
    with pytest.raises(ContaminatedTrainingWindowError):
        _det().fit(dirty, source_events=source)


def test_alarm_threshold_is_the_smallest_meeting_calib_fpr_on_the_clean_window():
    target, source = _corpus()
    det = _det(calib_fpr=0.3).fit(target, source_events=source)
    clean = det.predict(_clean_window(target))
    res = det.predict(target)
    thr = res.meta["decision_threshold"]
    assert (clean.scores >= thr).mean() <= 0.3
    assert (clean.scores >= np.nextafter(thr, -np.inf)).mean() > 0.3
    assert np.array_equal(res.y_pred, (res.scores >= thr).astype(int))
    assert np.array_equal(clean.y_pred, (clean.scores >= thr).astype(int))
    assert clean.y_pred.any()


def test_a_threshold_above_every_possible_score_is_reported():
    target, source = _corpus()
    det = _det()
    det._positive_scores = lambda X: np.ones(X.shape[0])
    res = det.fit(target, source_events=source).predict(target)
    assert res.meta["threshold_can_alarm"] is False
    assert not res.y_pred.any()


def test_source_trained_scores_do_not_depend_on_the_target():
    target, source = _corpus()
    other, _ = _corpus(seed=6)
    a = _det().fit(target, source_events=source).predict(target)
    b = _det().fit(other, source_events=source).predict(target)
    assert np.allclose(a.scores, b.scores)


def test_window_scores_do_not_depend_on_later_evaluation_events():
    target, source = _corpus()
    det = _det().fit(target, source_events=source)
    full = det.predict(target)
    evals = [e for e in target if e.split == "eval"]
    head = det.predict(evals[: len(evals) // 2])
    assert np.allclose(full.scores[: len(head.scores)], head.scores)


def test_default_detector_is_not_degenerate_on_the_default_config(tmp_path):
    cfg = synthetic_config()
    generate_dataset(cfg, tmp_path)
    events = events_from_jsonl(tmp_path / "events.jsonl")
    source = events_from_jsonl(tmp_path / "source_events.jsonl")
    det = TransferDetector(window_size=20, step_size=5, random_state=42)
    res = det.fit(events, source_events=source).predict(events)
    assert res.y_pred.mean() < 0.5
    assert precision_recall_f1(res.y_true, res.y_pred)["mcc"] > 0.5
    assert false_alarm_rate(res.y_true, res.y_pred) <= 0.1


def test_single_class_source_is_rejected():
    target, source = _corpus()
    all_normal = [replace(e, is_anomaly=False) for e in source]
    with pytest.raises(ValueError, match="both normal and anomalous"):
        _det().fit(target, source_events=all_normal)


def test_scoring_requires_an_evaluation_split():
    target, source = _corpus()
    det = _det().fit(target, source_events=source)
    with pytest.raises(ValueError, match="evaluation"):
        det.predict([e for e in target if e.split == "train"])
