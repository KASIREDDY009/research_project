from __future__ import annotations

from synthetic_data import synthetic_config

from synthetic_logs import SyntheticLogGenerator


def test_generate_target_splits_and_timestamps():
    gen = SyntheticLogGenerator(seed=1)
    events = gen.generate_target(n_events=100, train_frac=0.5)
    assert len(events) == 100
    assert sum(1 for e in events if e.split == "train") == 50
    assert sum(1 for e in events if e.split == "eval") == 50
    ts = [e.timestamp_ms for e in events]
    assert ts == sorted(ts)
    assert all(not e.is_anomaly for e in events)


def test_generate_source_has_labels():
    gen = SyntheticLogGenerator(seed=2)
    source = gen.generate_source(n_events=80, anomaly_rate=0.15)
    assert len(source) == 80
    assert all(e.split == "source" for e in source)
    assert sum(1 for e in source if e.is_anomaly) >= 1


def test_dataset_meta_records_the_categories_actually_injected(tmp_path):
    import json

    from synthetic_logs import generate_dataset

    cfg = synthetic_config()
    cfg["generator"].update({"n_normal_events": 200, "n_source_events": 100})
    generate_dataset(cfg, tmp_path)
    meta = json.loads((tmp_path / "meta.json").read_text())
    assert meta["categories"] == cfg["injector"]["categories"]


def test_a_missing_generator_setting_stops_generation(tmp_path):
    import pytest

    from synthetic_logs import generate_dataset

    cfg = synthetic_config()
    del cfg["injector"]["fault_rate"]
    with pytest.raises(KeyError, match="fault_rate"):
        generate_dataset(cfg, tmp_path)
