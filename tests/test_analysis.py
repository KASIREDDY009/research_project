from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from sflad.pipeline.analysis import analyse, bootstrap_f1_gap, cochran_q, holm, mcnemar, render
from sflad.pipeline.train_eval import load_config

ROOT = Path(__file__).resolve().parents[1]
CFG = load_config(ROOT / "configs" / "default.yaml")


def _run(root: Path, name: str, rng: np.random.Generator, n: int = 400) -> Path:
    y = (rng.random(n) < 0.3).astype(int)
    cats = np.where(y == 1, rng.choice(["permission", "config", "timeout", "resource", "latency"], n), "none")
    strengths = [int(rng.choice([4000, 6000])) if c == "latency" else None for c in cats]
    control = (y == 0) & (np.arange(n) > n * 0.8)
    good = np.where(rng.random(n) < 0.95, y, 1 - y)
    weak = np.where(rng.random(n) < 0.7, y, 1 - y)
    gate = np.where(rng.random(n) < 0.6, y, 0)
    forest = np.where(gate == 1, 0, weak)
    rd = root / name / "orders"
    (rd / "processed").mkdir(parents=True)
    (rd / "processed" / "window_predictions.json").write_text(json.dumps({
        "y_true": y.tolist(), "window_categories": cats.tolist(), "control_windows": control.tolist(),
        "cold_start_windows": (np.arange(n) % 5 == 0).tolist(), "window_strengths_ms": strengths,
        "window_end_ms": (np.arange(n) * 1000).tolist(),
        "y_pred": {"source_free": np.maximum(gate, forest).tolist(), "transfer": good.tolist(),
                   "transfer_similar": good.tolist(), "threshold": np.zeros(n, int).tolist(),
                   "source_free_forest": forest.tolist(), "novelty_gate": gate.tolist(),
                   "source_free_source_features": weak.tolist()}}))
    (rd / "processed" / "results.json").write_text(json.dumps({"config": CFG}))
    return rd


def test_mcnemar_counts_discordant_windows_and_is_exact():
    y = np.array([1, 1, 1, 0])
    r = mcnemar(y, np.array([1, 1, 1, 0]), np.array([0, 0, 0, 0]))
    assert (r["only_first_right"], r["only_second_right"]) == (3, 0) and abs(r["p"] - 0.25) < 1e-12


def test_cochran_q_is_zero_for_identical_detectors_and_nan_without_disagreement():
    same = np.array([[1, 1], [0, 0], [1, 1]])
    assert np.isnan(cochran_q(same)["q"])
    q = cochran_q(np.array([[1, 0], [1, 0], [1, 0], [0, 0]]))
    assert q["q"] == pytest.approx(3.0) and 0 < q["p"] < 0.1


def test_holm_adjusts_in_order_and_skips_untestable_hypotheses():
    out = holm({"H1": 0.01, "H2": 0.04, "H3": float("nan"), "H4": 0.03}, 0.05)
    assert out["H1"]["adjusted_p"] == pytest.approx(0.03) and out["H1"]["reject"] is True
    assert out["H4"]["adjusted_p"] == pytest.approx(0.06) and out["H4"]["reject"] is False
    assert out["H2"]["reject"] is False and out["H3"]["adjusted_p"] is None


def test_runs_with_different_detectors_stop_the_analysis(tmp_path):
    rng = np.random.default_rng(0)
    runs = [_run(tmp_path, f"c{i}", rng) for i in range(2)]
    # One run without the similar-application baseline.
    payload = json.loads((runs[1] / "processed" / "window_predictions.json").read_text())
    del payload["y_pred"]["transfer_similar"]
    (runs[1] / "processed" / "window_predictions.json").write_text(json.dumps(payload))
    cfg = dict(CFG, analysis={**CFG["analysis"], "bootstrap_samples": 50})
    with pytest.raises(ValueError, match="detectors"):
        analyse(runs, cfg)


def test_h1_carries_a_fault_segment_check_alongside_the_window_test(tmp_path):
    """H1/H2 report a window-level and a fault-segment McNemar test; the segment test is outside the Holm-Bonferroni family."""
    rng = np.random.default_rng(3)
    runs = [_run(tmp_path, f"c{i}", rng) for i in range(2)]
    cfg = dict(CFG, analysis={**CFG["analysis"], "bootstrap_samples": 50})
    result = analyse(runs, cfg)
    tests = result["families"]["source_free"]["tests"]
    sm = tests["H1"]["segment_mcnemar"]
    assert sm["n_segments"] > 0
    assert set(sm["n_detected"]) == {"transfer", "source_free"}
    assert 0 <= sm["n_detected"]["transfer"] <= sm["n_segments"]
    assert "p" in sm and (sm["p"] != sm["p"] or 0.0 <= sm["p"] <= 1.0)  # a real p or NaN, never absent
    assert "segment_mcnemar" not in tests["holm"]  # supplementary check, not part of the corrected family


def test_analysis_pools_runs_and_reports_every_hypothesis(tmp_path):
    rng = np.random.default_rng(0)
    runs = [_run(tmp_path, f"c{i}", rng) for i in range(3)]
    cfg = dict(CFG, analysis={**CFG["analysis"], "bootstrap_samples": 200})
    result = analyse(runs, cfg)
    assert result["windows"] == 1200
    t = result["families"]["source_free"]["tests"]
    assert t["H1"]["gap"] > 0 and t["H1"]["ci_low"] <= t["H1"]["gap"] <= t["H1"]["ci_high"]
    assert t["H1"]["p"] < 0.001 and t["holm"]["H1"]["reject"] is True
    assert t["H6"]["gap"] == 0 and np.isnan(t["H6"]["p"])
    assert set(t["H4"]["recall"]) == {"permission", "config", "timeout", "resource", "latency"}
    assert t["H1"]["ci_high"] >= t["H1"]["upper_one_sided_95"] >= t["H1"]["gap"]
    decisions = result["families"]["source_free"]["decisions"]
    assert set(decisions) == {"transfer", "transfer_similar"}
    assert decisions["transfer"] == {"non_inferior": False, "above_threshold_alarms": True, "viable_substitute": False}
    assert t["H5"]["detectors"] == ["source_free", "transfer", "transfer_similar", "threshold"]
    sup = result["supplementary"]
    g = sup["novelty_gate"]
    assert g["alarms"] == g["alarms_from_the_gate_only"] + g["alarms_from_the_forest_only"] + g["alarms_from_both"]
    assert g["alarms_from_both"] == 0 and g["alarms_from_the_gate_only"] > 0
    pooled = result["pooled"]
    assert sup["feature_space"]["gap"] == pytest.approx(pooled["transfer"]["f1"] - pooled["source_free_source_features"]["f1"])
    assert set(sup["latency_recall_by_delay"]) == {"4000", "6000"}
    parts = sup["elasticity_false_alarms"]
    assert parts["with_new_environment"]["windows"] + parts["without_new_environment"]["windows"] == result["elasticity_windows"]
    text = render(result)
    assert "H5" in text and "Non-inferior" in text and "Novelty gate" in text


def test_one_holm_family_per_application_with_shared_h5_and_h6(tmp_path):
    rng = np.random.default_rng(5)
    runs = [_run(tmp_path, f"c{i}", rng) for i in range(2)]
    result = analyse(runs, dict(CFG, analysis={**CFG["analysis"], "bootstrap_samples": 50}))
    assert set(result["holm"]) == {"H1:source_free", "H3:source_free", "H4:source_free", "H5", "H6"}
    assert result["families"]["source_free"]["tests"]["holm"]["H6"] is result["holm"]["H6"]


def test_runs_scored_with_a_different_config_stop_the_analysis(tmp_path):
    rng = np.random.default_rng(6)
    runs = [_run(tmp_path, f"c{i}", rng) for i in range(2)]
    (runs[1] / "processed" / "results.json").write_text(json.dumps({"config": dict(CFG, seed=1)}))
    with pytest.raises(ValueError, match="different config"):
        analyse(runs, dict(CFG, analysis={**CFG["analysis"], "bootstrap_samples": 50}))


def _f1(y, p, w):
    tp, fp, fn = (w * (y & p)).sum(), (w * (~y & p)).sum(), (w * (y & ~p)).sum()
    return 2 * tp / (2 * tp + fp + fn)


def test_bootstrap_gap_resamples_windows_within_each_run():
    rng = np.random.default_rng(1)
    runs = []
    for n in (30, 50):
        y = (rng.random(n) < 0.4).astype(int)
        runs.append({"y_true": y, "y_pred": {"a": np.where(rng.random(n) < 0.8, y, 1 - y), "b": np.zeros(n, int)}})
    out = bootstrap_f1_gap(runs, "a", "b", 400, np.random.default_rng(7))
    assert out == bootstrap_f1_gap(runs, "a", "b", 400, np.random.default_rng(7))
    y = np.concatenate([r["y_true"] for r in runs]).astype(bool)
    pa = np.concatenate([r["y_pred"]["a"] for r in runs]).astype(bool)
    pb = np.concatenate([r["y_pred"]["b"] for r in runs]).astype(bool)
    check = np.random.default_rng(7)
    gaps = []
    for _ in range(400):
        w = np.concatenate([np.bincount(check.integers(0, n, n), minlength=n) for n in (30, 50)]).astype(float)
        gaps.append(_f1(y, pa, w) - _f1(y, pb, w))
    assert out["gap"] == pytest.approx(_f1(y, pa, np.ones(80)) - _f1(y, pb, np.ones(80)))
    assert [out["ci_low"], out["ci_high"], out["upper_one_sided_95"]] == pytest.approx(np.percentile(gaps, [2.5, 97.5, 95.0]))
    assert out["ci_low"] < out["gap"] < out["ci_high"] and out["n_undefined_resamples"] == 0


def test_non_inferior_and_viable_when_the_source_free_detector_matches_the_baseline(tmp_path):
    rng = np.random.default_rng(5)
    runs = [_run(tmp_path, f"c{i}", rng) for i in range(2)]
    cfg = dict(CFG, analysis={**CFG["analysis"], "bootstrap_samples": 200})
    for rd in runs:
        path = rd / "processed" / "window_predictions.json"
        payload = json.loads(path.read_text())
        payload["y_pred"]["source_free"] = payload["y_pred"]["transfer"]
        path.write_text(json.dumps(payload))
    decision = analyse(runs, cfg)["families"]["source_free"]["decisions"]["transfer"]
    assert decision == {"non_inferior": True, "above_threshold_alarms": True, "viable_substitute": True}
    for rd in runs:
        path = rd / "processed" / "window_predictions.json"
        payload = json.loads(path.read_text())
        payload["y_pred"]["threshold"] = payload["y_pred"]["transfer"]
        path.write_text(json.dumps(payload))
    decision = analyse(runs, cfg)["families"]["source_free"]["decisions"]["transfer"]
    assert decision == {"non_inferior": True, "above_threshold_alarms": False, "viable_substitute": False}
