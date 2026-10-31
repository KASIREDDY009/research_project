from __future__ import annotations

import numpy as np

from sflad.detectors.base import window_features, window_template_shares


def test_shares_are_counts_over_known_templates_per_window():
    vocab = {"a": 0, "b": 1, "c": 2}
    X, ends = window_template_shares(["a", "a", "b", "zzz", "c", "c"], vocab, window_size=3, step_size=3)
    assert ends.tolist() == [2, 5]
    assert np.allclose(X.toarray(), [[2 / 3, 1 / 3, 0.0], [0.0, 0.0, 1.0]])
    assert X.nnz == 3


def test_a_window_without_known_templates_is_a_zero_row_and_dense_matches_sparse():
    vocab = {"a": 0}
    X, _ = window_template_shares(["x", "y", "a"], vocab, window_size=2, step_size=1)
    assert X.toarray().tolist() == [[0.0], [1.0]]
    dense, _ = window_features(["x", "y", "a"], vocab, window_size=2, step_size=1)
    assert np.array_equal(dense, X.toarray())


def test_a_window_is_faulty_when_any_of_its_lines_is_faulty():
    from sflad.data.schema import LogEvent
    from sflad.detectors.base import window_end_indices, window_labels

    faulty = {3, 4, 9}
    events = [LogEvent(timestamp_ms=i, message="m", is_anomaly=i in faulty) for i in range(10)]
    ends = window_end_indices(len(events), window_size=4, step_size=4)
    assert ends.tolist() == [3, 7]
    assert window_labels(events, ends, window_size=4).tolist() == [1, 1]
    clean_second = [LogEvent(timestamp_ms=i, message="m", is_anomaly=i == 3) for i in range(10)]
    assert window_labels(clean_second, ends, window_size=4).tolist() == [1, 0]
