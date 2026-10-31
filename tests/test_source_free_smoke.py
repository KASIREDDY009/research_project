from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from synthetic_faults import FaultInjector
from synthetic_logs import SyntheticLogGenerator
from sflad.detectors.source_free import SourceFreeDetector
from sflad.detectors.threshold import ThresholdDetector
from sflad.detectors.transfer import TransferDetector
from sflad.pipeline.metrics import summarise_result

KEYWORDS = yaml.safe_load(
    (Path(__file__).resolve().parents[1] / "configs" / "default.yaml").read_text()
)["detectors"]["threshold"]["error_keywords"]


def _small_corpus():
    gen = SyntheticLogGenerator(seed=99)
    target = gen.generate_target(120, train_frac=0.5)
    target = FaultInjector(seed=99).inject(
        target,
        fault_rate=0.15,
        inject_after_frac=0.5,
        min_fault_gap_events=3,
        categories=["permission", "config", "timeout", "resource"],
        fault_burst_size=2,
    )
    source = gen.generate_source(80, anomaly_rate=0.15)
    return target, source


def test_source_free_smoke():
    target, _ = _small_corpus()
    det = SourceFreeDetector(
        window_size=10,
        step_size=5,
        calib_fpr=0.1,
        random_state=0,
    )
    det.fit(target)
    res = det.predict(target)
    assert len(res.y_pred) == len(res.y_true)
    assert res.y_pred.dtype == int or res.y_pred.dtype == res.y_true.dtype
    m = summarise_result(res.y_true, res.y_pred)
    assert 0.0 <= m["f1"] <= 1.0


def test_source_free_transfer_and_threshold_smoke():
    target, source = _small_corpus()
    sf = SourceFreeDetector(window_size=10, step_size=5, random_state=1)
    tr = TransferDetector(window_size=10, step_size=5, random_state=1)
    th = ThresholdDetector(KEYWORDS, window_size=10, step_size=5)
    sf.fit(target)
    tr.fit(target, source_events=source)
    th.fit(target)
    for det in (sf, tr, th):
        r = det.predict(target)
        assert len(r.y_true) > 0


def test_scoring_requires_an_evaluation_split():
    target, source = _small_corpus()
    train_only = [e for e in target if e.split == "train"]
    sf = SourceFreeDetector(window_size=10, step_size=5, random_state=1)
    th = ThresholdDetector(KEYWORDS, window_size=10, step_size=5)
    for det in (sf.fit(target), th.fit(target)):
        with pytest.raises(ValueError, match="evaluation"):
            det.predict(train_only)


def test_novelty_gate_count_is_absent_when_the_gate_is_off():
    target, _ = _small_corpus()
    kw = dict(window_size=10, step_size=5, random_state=1)
    off = SourceFreeDetector(use_novelty_gate=False, **kw).fit(target).predict(target)
    on = SourceFreeDetector(**kw).fit(target).predict(target)
    assert off.meta["n_novelty_gate_windows"] is None
    assert isinstance(on.meta["n_novelty_gate_windows"], int)


def test_the_threshold_detector_refuses_an_empty_keyword_list():
    with pytest.raises(ValueError, match="keyword"):
        ThresholdDetector([])
