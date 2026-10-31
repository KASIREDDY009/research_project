from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pytest

from sflad.detectors.base import KEYWORD_GROUPS
from sflad.detectors.transfer import TransferDetector
from synthetic_data import synthetic_config

ROOT = Path(__file__).resolve().parents[1]


def _cfg():
    from sflad.pipeline.train_eval import load_config

    cfg = load_config(ROOT / "configs" / "default.yaml")
    cfg["detectors"]["source_free_deeplog"].update({"epochs": 2, "hidden": 16, "embed_dim": 8, "layers": 1})
    return cfg


def _run(cfg, tmp_path):
    from synthetic_logs import generate_dataset
    from sflad.pipeline.train_eval import run_experiment

    paths = generate_dataset(synthetic_config(int(cfg["seed"])), tmp_path / "syn")
    return run_experiment(cfg, paths["events"], paths["source_events"], tmp_path / "processed")


ARMS = ["source_free", "source_free_deeplog", "transfer", "threshold", "source_free_forest", "novelty_gate",
        "source_free_source_features"]


def test_detectors_report_mcc_and_forfeiture(tmp_path):
    payload = _run(_cfg(), tmp_path)
    assert list(payload["summaries"]) == ARMS
    for s in payload["summaries"].values():
        assert "mcc" in s
    assert set(payload["forfeiture"]) == {f"{m}:{p}" for m in ("f1", "mcc") for p in (
        "transfer-source_free", "transfer-source_free_deeplog", "transfer-source_free_source_features")}
    assert all(value is not None for value in payload["forfeiture"].values())
    summary = (tmp_path / "processed" / "summary.txt").read_text()
    assert "MCC" in summary and "DeepLog" in summary


def test_similar_and_openstack_sources_add_baselines_and_their_forfeitures(tmp_path):
    from synthetic_logs import generate_dataset
    from sflad.pipeline.train_eval import run_experiment

    cfg = _cfg()
    target = generate_dataset(synthetic_config(int(cfg["seed"])), tmp_path / "syn")
    similar = generate_dataset(synthetic_config(int(cfg["seed"]) + 1), tmp_path / "other")
    payload = run_experiment(cfg, target["events"], target["source_events"], tmp_path / "processed",
                             similar_source_path=similar["events"], openstack_source_path=target["source_events"])
    s = payload["summaries"]
    assert list(s) == ARMS[:3] + ["transfer_openstack", "transfer_similar"] + ARMS[3:]
    assert payload["forfeiture"]["f1:transfer_similar-source_free"] == s["transfer_similar"]["f1"] - s["source_free"]["f1"]
    assert payload["forfeiture"]["f1:transfer_openstack-source_free_deeplog"] == (
        s["transfer_openstack"]["f1"] - s["source_free_deeplog"]["f1"])
    summary = (tmp_path / "processed" / "summary.txt").read_text()
    assert "Similar-application baseline" in summary and "OpenStack-trained baseline" in summary


def test_every_label_free_threshold_uses_the_shared_false_alarm_target(tmp_path):
    cfg = _cfg()
    cfg["detectors"]["calib_fpr"] = 0.037
    meta = _run(cfg, tmp_path)["detector_meta"]
    for arm in ("source_free", "source_free_deeplog", "transfer", "source_free_forest", "source_free_source_features"):
        assert meta[arm]["calib_fpr"] == 0.037
    for arm, m in meta.items():
        assert set(m["seconds"]) == {"fit", "predict"}


def test_the_fault_free_window_is_split_into_a_training_and_a_calibration_part(tmp_path):
    cfg = _cfg()
    meta = _run(cfg, tmp_path)["detector_meta"]
    cfg["detectors"]["calib_share"] = 0.25
    other = _run(cfg, tmp_path / "quarter")["detector_meta"]
    assert other["source_free"]["n_calib_windows"] < meta["source_free"]["n_calib_windows"]
    assert other["source_free"]["n_train_windows"] > meta["source_free"]["n_train_windows"]
    assert other["transfer"]["n_calib_windows"] == other["source_free"]["n_calib_windows"]


def test_every_fitted_detector_is_saved_and_reloads_to_the_same_alarms(tmp_path):
    import joblib
    import numpy as np

    from sflad.data.event_io import events_from_jsonl

    payload = _run(_cfg(), tmp_path)
    saved = json.loads((tmp_path / "processed" / "window_predictions.json").read_text())
    events = events_from_jsonl(tmp_path / "syn" / "events.jsonl")
    assert list(payload["models"]) == ARMS
    for name, path in payload["models"].items():
        detector = joblib.load(tmp_path / "processed" / path)
        assert np.array_equal(detector.predict(events).y_pred, saved["y_pred"][name])


def test_the_demo_scores_a_saved_model(tmp_path, capsys):
    from scripts.scoring.demo_detect import main

    payload = _run(_cfg(), tmp_path)
    model = str(tmp_path / "processed" / payload["models"]["source_free"])
    assert main([model, "--events", str(tmp_path / "syn" / "events.jsonl")]) == 0
    out = capsys.readouterr().out
    assert "windows of 20 lines" in out and "F1" in out


def test_results_record_the_effective_configuration(tmp_path):
    cfg = _cfg()
    _run(cfg, tmp_path)
    saved = json.loads((tmp_path / "processed" / "results.json").read_text())
    assert saved["config"]["detectors"] == cfg["detectors"]
    assert saved["lexical_keyword_groups"] == KEYWORD_GROUPS


def test_forfeiture_is_the_measured_gap_between_the_arms(tmp_path, monkeypatch):
    cfg = _cfg()
    # A baseline that can never alarm makes every gap measurable and non-zero.
    monkeypatch.setattr(TransferDetector, "_positive_scores", lambda self, X: np.ones(X.shape[0]))
    payload = _run(cfg, tmp_path)
    s, forfeiture = payload["summaries"], payload["forfeiture"]
    assert forfeiture["f1:transfer-source_free"] == s["transfer"]["f1"] - s["source_free"]["f1"] != 0.0
    assert forfeiture["f1:transfer-source_free_deeplog"] == s["transfer"]["f1"] - s["source_free_deeplog"]["f1"] != 0.0
    # The baseline raises no alarm, so its MCC is undefined and so is every MCC gap.
    assert math.isnan(s["transfer"]["mcc"])
    assert math.isnan(forfeiture["mcc:transfer-source_free"]) and math.isnan(forfeiture["mcc:transfer-source_free_deeplog"])


@pytest.mark.parametrize(
    "path",
    [
        ("detectors", "calib_fpr"),
        ("metrics", "eval_sanity", "min_positives"),
    ],
)
def test_a_missing_setting_stops_the_run_before_any_output(tmp_path, path):
    cfg = _cfg()
    parent = cfg
    for key in path[:-1]:
        parent = parent[key]
    del parent[path[-1]]
    with pytest.raises(KeyError, match=path[-1]):
        _run(cfg, tmp_path)
    assert not (tmp_path / "processed").exists()


def test_a_missing_configuration_file_is_an_error():
    from sflad.pipeline.train_eval import load_config

    with pytest.raises(FileNotFoundError):
        load_config(ROOT / "configs" / "no_such_file.yaml")
