from __future__ import annotations

from synthetic_data import synthetic_config

from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from sflad.data.schema import LogEvent
from synthetic_logs import generate_dataset
from sflad.detectors.base import UNK_TOKEN, ContaminatedTrainingWindowError
from sflad.detectors.deeplog import DeepLogDetector
from sflad.pipeline.metrics import false_alarm_rate, precision_recall_f1
from sflad.pipeline.train_eval import events_from_jsonl

ROOT = Path(__file__).resolve().parents[1]

CYCLE = ["start job", "load data", "save result", "finish job"]


def _events(keys, split):
    return [LogEvent(timestamp_ms=i, message=k, split=split) for i, k in enumerate(keys)]


def _det(**kw):
    base = dict(
        history=3, hidden=16, layers=1, embed_dim=8, epochs=40, lr=0.01, batch_size=16,
        window_size=8, step_size=8, random_state=0,
    )
    base.update(kw)
    return DeepLogDetector(**base)


def test_learns_cycle_and_flags_only_the_disordered_window():
    det = _det().fit(_events(CYCLE * 50, "train"))
    assert det.g == 1  # a deterministic cycle needs only the top-1 prediction
    eval_keys = CYCLE * 4
    eval_keys[9] = "start job"  # position 9 should be 'load data'
    res = det.predict(_events(eval_keys, "eval"))
    assert np.flatnonzero(res.y_pred).tolist() == [1]  # window 1 covers events 8..15


def test_unseen_template_is_flagged():
    det = _det().fit(_events(CYCLE * 50, "train"))
    eval_keys = CYCLE * 4
    eval_keys[5] = "kernel panic detected"
    assert det.predict(_events(eval_keys, "eval")).y_pred[0] == 1


def test_contaminated_training_window_fails_loudly():
    train = _events(CYCLE * 10, "train")
    train[4] = replace(train[4], is_anomaly=True)
    with pytest.raises(ContaminatedTrainingWindowError):
        _det().fit(train)


def test_too_short_training_window_is_rejected():
    with pytest.raises(ValueError):
        _det(history=10).fit(_events(CYCLE, "train"))


def test_predictions_ignore_evaluation_labels():
    det = _det().fit(_events(CYCLE * 50, "train"))
    ev = _events(CYCLE * 4, "eval")
    flipped = [replace(e, is_anomaly=True) for e in ev]
    assert np.array_equal(det.predict(ev).y_pred, det.predict(flipped).y_pred)


def test_default_detector_is_not_degenerate_on_the_default_config(tmp_path):
    cfg = synthetic_config()
    generate_dataset(cfg, tmp_path)
    events = events_from_jsonl(tmp_path / "events.jsonl")
    det = DeepLogDetector(window_size=20, step_size=5, random_state=42)
    res = det.fit(events).predict(events)
    assert res.y_pred.mean() < 0.5
    assert precision_recall_f1(res.y_true, res.y_pred)["mcc"] > 0.5
    assert false_alarm_rate(res.y_true, res.y_pred) <= 0.1
    assert res.meta["n_calib_windows"] > 0


def test_calibration_counts_windows_not_events(monkeypatch):
    det = _det(window_size=20, step_size=20, calib_fpr=0.2)
    det.vocab = {k: i for i, k in enumerate("abcdefgh")}
    ranks = np.ones(100, dtype=int)
    ranks[5::20] = 3  # one rank-3 event per window: 5% of events, every window
    ranks[45] = 5  # one of the five windows also holds a rank-5 event
    monkeypatch.setattr(det, "_event_flags", lambda seq: (np.zeros(100, dtype=int), ranks))
    assert det._calibrate_g(np.zeros(100, dtype=np.int64)) == 3
    assert det.n_calib_windows == 5


def test_calibration_windows_with_an_unseen_key_use_up_the_allowance(monkeypatch):
    det = _det(window_size=20, step_size=20, calib_fpr=0.2)
    ranks = np.ones(100, dtype=int)
    ranks[5::20] = 3
    ranks[45] = 5
    unknown = np.zeros(100, dtype=int)
    unknown[70] = 1  # one window alarms whatever g is: it takes the one alarm allowed
    monkeypatch.setattr(det, "_event_flags", lambda seq: (unknown, ranks))
    assert det._calibrate_g(np.zeros(100, dtype=np.int64)) == 5


def test_unseen_template_is_flagged_even_when_every_rank_is_accepted():
    det = _det().fit(_events(CYCLE * 50, "train"))
    det.g = len(det.vocab)  # every known key is accepted
    eval_keys = CYCLE * 4
    eval_keys[5] = "kernel panic detected"
    assert np.flatnonzero(det.predict(_events(eval_keys, "eval")).y_pred).tolist() == [0]


def test_the_unseen_key_output_never_outranks_a_known_key():
    import torch

    det = _det().fit(_events(CYCLE * 50, "train"))
    logits = torch.zeros(1, len(det.vocab))
    logits[0, det.vocab[UNK_TOKEN]] = 10.0
    logits[0, 0] = 5.0
    det.model = lambda x: logits.clone()
    assert det._ranks(np.zeros((1, det.history), dtype=np.int64), np.array([0])).tolist() == [1]


def test_training_part_must_exceed_history():
    with pytest.raises(ValueError, match="training part"):
        _det(history=10).fit(_events(CYCLE * 3, "train"))  # 12 events: training part 6, calibration part 6


def test_calibration_part_must_hold_a_full_window():
    with pytest.raises(ValueError, match="calibration part"):
        _det(window_size=20, step_size=20).fit(_events(CYCLE * 8, "train"))  # calibration part 16 < 20


def test_scoring_requires_an_evaluation_split():
    det = _det().fit(_events(CYCLE * 50, "train"))
    with pytest.raises(ValueError, match="evaluation"):
        det.predict(_events(CYCLE * 4, "train"))
