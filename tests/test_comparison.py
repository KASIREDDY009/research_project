from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from sflad.pipeline.comparison import compare_runs, describe


def _run(out_dir: Path, name: str, f1_if: float, f1_tr: float) -> Path:
    rd = out_dir / name
    (rd / "raw").mkdir(parents=True)
    (rd / "processed").mkdir()
    (rd / "raw" / "episodes.jsonl").write_text('{"burst_faulty": 2}\n{"burst_faulty": 0}\n{"burst_faulty": 1}\n')
    (rd / "raw" / "run.json").write_text(json.dumps({"config": {"faults": {"injections_per_category": 60,
                                                                           "categories": ["permission"]}}}))
    arm = lambda f1: {"precision": 1.0, "recall": f1, "f1": f1, "mcc": float("nan"), "false_alarm_rate": 0.0}
    payload = {
        "config": {"seed": 42},
        "label_stats": {"n": 100.0, "support_pos": 10.0},
        "summaries": {"source_free": arm(f1_if), "transfer": arm(f1_tr)},
        "forfeiture": {"f1_if": f1_tr - f1_if, "mcc_if": float("nan")},
    }
    (rd / "processed" / "results.json").write_text(json.dumps(payload))
    return rd


def test_describe_counts_undefined_values():
    s = describe([0.5, float("nan"), 0.7])
    assert s["n"] == 2 and s["n_undefined"] == 1
    assert math.isclose(s["mean"], 0.6) and s["min"] == 0.5 and s["max"] == 0.7
    assert describe([0.5])["std"] is None and describe([])["mean"] is None


def test_runs_are_listed_and_summarised_from_their_own_records(tmp_path):
    runs = [_run(tmp_path, "run1", 0.2, 0.9), _run(tmp_path, "run2", 0.9, 0.9)]
    comparison = compare_runs(tmp_path / "out", runs)
    first = comparison["per_run"][0]
    assert first["run"].endswith("/run1") and first["injections_per_category"] == 60
    assert first["n_fault_episodes"] == 3 and first["n_silent_episodes"] == 1
    forf = comparison["aggregate"]["forfeiture"]
    assert math.isclose(forf["f1_if"]["mean"], 0.35)
    assert forf["mcc_if"]["n"] == 0 and forf["mcc_if"]["n_undefined"] == 2
    assert "| " in (tmp_path / "out" / "comparison.md").read_text()


def test_runs_with_different_detectors_are_rejected(tmp_path):
    a = _run(tmp_path, "run1", 0.2, 0.9)
    b = _run(tmp_path, "run2", 0.9, 0.9)
    payload = json.loads((b / "processed" / "results.json").read_text())
    del payload["summaries"]["transfer"]
    (b / "processed" / "results.json").write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="different detectors"):
        compare_runs(tmp_path / "out", [a, b])


def test_runs_with_different_configs_are_rejected(tmp_path):
    a = _run(tmp_path, "run1", 0.2, 0.9)
    b = _run(tmp_path, "run2", 0.9, 0.9)
    payload = json.loads((b / "processed" / "results.json").read_text())
    payload["config"]["seed"] = 1
    (b / "processed" / "results.json").write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="different config"):
        compare_runs(tmp_path / "out", [a, b])
