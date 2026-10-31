from __future__ import annotations

import numpy as np

from sflad.pipeline.metrics import (
    delay_summary,
    false_alarm_rate,
    precision_recall_f1,
    segment_delays,
    segment_hits,
    summarise_result,
)


def test_precision_recall_f1_perfect():
    y = np.array([0, 1, 1, 0, 1])
    m = precision_recall_f1(y, y)
    assert m["precision"] == 1.0
    assert m["recall"] == 1.0
    assert m["f1"] == 1.0


def test_false_alarm_rate():
    y_true = np.array([0, 0, 0, 1])
    y_pred = np.array([1, 0, 0, 1])
    assert abs(false_alarm_rate(y_true, y_pred) - 1 / 3) < 1e-9


def test_summary_holds_the_window_measures():
    y_true = np.array([0, 0, 1, 1, 0, 1, 0])
    y_pred = np.array([0, 0, 0, 1, 0, 1, 0])
    s = summarise_result(y_true, y_pred)
    assert s["f1"] == 0.8 and s["false_alarm_rate"] == 0.0


def test_mcc_known_values():
    y = np.array([0, 1, 1, 0, 1])
    assert precision_recall_f1(y, y)["mcc"] == 1.0
    assert precision_recall_f1(y, 1 - y)["mcc"] == -1.0
    # tp=2, fn=1, fp=1, tn=2 -> (2*2 - 1*1) / sqrt(3*3*3*3) = 1/3
    y_true = np.array([1, 1, 1, 0, 0, 0])
    y_pred = np.array([1, 1, 0, 1, 0, 0])
    assert abs(precision_recall_f1(y_true, y_pred)["mcc"] - 1 / 3) < 1e-9
    # undefined denominator (an empty confusion-matrix row or column) -> NaN, never 0
    assert np.isnan(precision_recall_f1(np.zeros(4, int), np.zeros(4, int))["mcc"])


def test_undefined_metrics_are_nan():
    missed = precision_recall_f1(np.array([1, 0, 0]), np.array([0, 0, 0]))
    assert np.isnan(missed["precision"]) and np.isnan(missed["mcc"])
    assert missed["recall"] == 0.0 and missed["f1"] == 0.0  # a missed fault is a measured zero
    no_positives = precision_recall_f1(np.array([0, 0]), np.array([1, 0]))
    assert np.isnan(no_positives["recall"]) and np.isnan(no_positives["f1"])
    assert no_positives["precision"] == 0.0
    assert np.isnan(false_alarm_rate(np.array([1, 1]), np.array([1, 0])))


def test_f1_from_counts_matches_precision_recall_form():
    y_true = np.array([1, 1, 1, 0, 0, 0, 1])
    y_pred = np.array([1, 0, 1, 1, 0, 0, 0])
    m = precision_recall_f1(y_true, y_pred)
    assert abs(m["f1"] - 2 * m["precision"] * m["recall"] / (m["precision"] + m["recall"])) < 1e-12


def test_clean_window_certificate(tmp_path):
    from sflad.pipeline.clean_window import (
        write_clean_window_certificate,
        require_clean_window_certificate,
    )
    from sflad.data.schema import normalize_fault_category

    path = tmp_path / "clean_window_certificate.json"
    write_clean_window_certificate(
        path,
        train_start="0",
        train_end="100",
        n_events=10,
        n_failed_call_lines=0,
        seed=42,
    )
    data = require_clean_window_certificate(path)
    assert data["status"] == "certified_clean"
    assert normalize_fault_category(" Timeout ") == "timeout"


def test_segment_hits_is_one_bool_per_fault_segment():
    """One entry per run of consecutive fault windows; a segment counts only with an alarm inside it."""
    y_true = np.array([0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1])
    y_pred = np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0])
    assert segment_hits(y_true, y_pred).tolist() == [True, False, True]  # the alarm after segment 2 does not count


def test_segment_delays_count_from_the_first_fault_window_to_the_first_alarm_inside_the_segment():
    y_true = np.array([0, 1, 1, 1, 0, 1, 1, 0, 1])
    y_pred = np.array([1, 0, 0, 1, 1, 1, 0, 0, 0])
    end_ms = np.arange(9) * 2000
    d = segment_delays(y_true, y_pred, end_ms)
    assert [x["windows"] for x in d[:2]] == [2.0, 0.0] and [x["seconds"] for x in d[:2]] == [4.0, 0.0]
    assert np.isnan(d[2]["windows"]) and np.isnan(d[2]["seconds"])
    s = delay_summary(d)
    assert (s["n_segments"], s["n_detected_segments"], s["mean_delay_windows"], s["median_delay_seconds"]) == (3, 2, 1.0, 2.0)
    assert delay_summary(segment_delays(y_true, np.zeros(9, int), end_ms))["median_delay_seconds"] is None
