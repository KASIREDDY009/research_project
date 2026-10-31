from __future__ import annotations

from synthetic_data import synthetic_config

from synthetic_faults import FaultInjector
from synthetic_logs import SyntheticLogGenerator


def test_injector_only_after_frac_and_categories():
    gen = SyntheticLogGenerator(seed=3)
    base = gen.generate_target(200, train_frac=0.5)
    inj = FaultInjector(seed=3)
    out = inj.inject(
        base,
        fault_rate=0.1,
        inject_after_frac=0.5,
        categories=["permission", "timeout"],
        min_fault_gap_events=5,
        fault_burst_size=2,
    )
    train_anom = [e for e in out if e.split == "train" and e.is_anomaly]
    eval_anom = [e for e in out if e.split == "eval" and e.is_anomaly]
    assert train_anom == []
    assert len(eval_anom) >= 1
    cats = {e.fault_category for e in eval_anom}
    assert cats <= {"permission", "timeout"}
    assert all(e.level == "ERROR" for e in eval_anom)


def test_the_same_seed_gives_byte_identical_data(tmp_path):
    from synthetic_logs import generate_dataset

    cfg = synthetic_config()
    generate_dataset(cfg, tmp_path / "a")
    generate_dataset(cfg, tmp_path / "b")
    for name in ("events.jsonl", "source_events.jsonl"):
        assert (tmp_path / "a" / name).read_bytes() == (tmp_path / "b" / name).read_bytes()
