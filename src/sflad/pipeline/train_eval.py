"""Train and evaluate every configured detector on one shared window grid."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, Optional

import joblib
import numpy as np
import yaml

from sflad.data.event_io import events_from_jsonl
from sflad.detectors.base import KEYWORD_GROUPS
from sflad.detectors.deeplog import DeepLogDetector
from sflad.detectors.source_free import SourceFeatureForest, SourceFreeDetector
from sflad.detectors.threshold import ThresholdDetector
from sflad.detectors.transfer import TransferDetector
from sflad.pipeline.clean_window import require_clean_window_certificate
from sflad.pipeline.eval_sanity import assert_eval_label_sanity
from sflad.pipeline.metrics import delay_summary, segment_delays, summarise_result, window_fault_categories


def load_config(path: Path) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def transfer_detector(cfg: Dict[str, Any], window: int, step: int, **overrides: Any) -> TransferDetector:
    """The labelled-source baseline as configured; overrides replace single settings (e.g. the seed)."""
    tr_cfg = cfg["detectors"]["transfer"]
    settings: Dict[str, Any] = dict(
        n_estimators=int(tr_cfg["n_estimators"]),
        max_depth=int(tr_cfg["max_depth"]),
        class_weight=tr_cfg["class_weight"],
        window_size=window,
        step_size=step,
        random_state=int(cfg["seed"]),
        calib_fpr=float(cfg["detectors"]["calib_fpr"]),
        calib_share=float(cfg["detectors"]["calib_share"]),
    )
    settings.update(overrides)
    return TransferDetector(**settings)


# Arm name -> role. The primary arms answer the research question; the ablation arms show what the
# novelty gate and the feature space contribute; the threshold alarms are the operational reference.
ARM_ROLES = {
    "source_free": "Source-free (Isolation Forest with novelty gate)",
    "source_free_deeplog": "Source-free (DeepLog-style)",
    "transfer": "BGL-trained baseline",
    "transfer_openstack": "OpenStack-trained baseline",
    "transfer_similar": "Similar-application baseline",
    "threshold": "Threshold alarms",
    "source_free_forest": "Ablation: Isolation Forest alone",
    "novelty_gate": "Ablation: novelty gate alone",
    "source_free_source_features": "Ablation: source-free detector on the BGL baseline's features",
}
SOURCE_FREE_ARMS = ("source_free", "source_free_deeplog")
BASELINE_ARMS = ("transfer", "transfer_openstack", "transfer_similar")


def run_experiment(
    cfg: Dict[str, Any],
    events_path: Path,
    source_path: Path,
    processed_dir: Path,
    clean_window_certificate: Optional[Path] = None,
    similar_source_path: Optional[Path] = None,
    openstack_source_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """Every detector on one event file; the certificate comes from the evaluation run that produced
    the events. source_path is the BGL-trained baseline's labelled source; with openstack_source_path or
    similar_source_path, the OpenStack-trained and similar-application baselines train on those labelled
    events beside it."""
    events = events_from_jsonl(events_path)
    source_events = events_from_jsonl(source_path)

    fcfg = cfg["features"]
    dcfg = cfg["detectors"]
    mcfg = cfg["metrics"]
    scfg = mcfg["eval_sanity"]
    seed = int(cfg["seed"])
    window = int(fcfg["window_size"])
    step = int(fcfg["step_size"])
    split = dict(calib_fpr=float(dcfg["calib_fpr"]), calib_share=float(dcfg["calib_share"]),
                 train_share=float(dcfg["train_share"]))
    sanity_kw = {
        "max_pos_rate": float(scfg["max_pos_rate"]),
        "min_pos_rate": float(scfg["min_pos_rate"]),
        "min_negatives": int(scfg["min_negatives"]),
        "min_positives": int(scfg["min_positives"]),
    }

    sf_cfg = dcfg["source_free"]
    th_cfg = dcfg["threshold"]
    dl_cfg = dcfg["source_free_deeplog"]

    def isolation(**parts: bool) -> SourceFreeDetector:
        return SourceFreeDetector(n_estimators=int(sf_cfg["n_estimators"]), window_size=window, step_size=step,
                                  random_state=seed, **split, **parts)

    dl = DeepLogDetector(
        history=int(dl_cfg["history"]),
        hidden=int(dl_cfg["hidden"]),
        layers=int(dl_cfg["layers"]),
        embed_dim=int(dl_cfg["embed_dim"]),
        epochs=int(dl_cfg["epochs"]),
        lr=float(dl_cfg["lr"]),
        batch_size=int(dl_cfg["batch_size"]),
        window_size=window,
        step_size=step,
        random_state=seed,
        **split,
    )
    th = ThresholdDetector(
        error_keywords=list(th_cfg["error_keywords"]),
        window_size=window,
        step_size=step,
        min_keyword_count=int(th_cfg["min_keyword_count"]),
    )
    bgl = {"source_events": source_events}
    arms = [("source_free", isolation(use_forest=True, use_novelty_gate=True), {}),
            ("source_free_deeplog", dl, {}),
            ("transfer", transfer_detector(cfg, window, step), bgl)]
    if openstack_source_path is not None:
        arms.append(("transfer_openstack", transfer_detector(cfg, window, step),
                     {"source_events": events_from_jsonl(openstack_source_path)}))
    if similar_source_path is not None:
        arms.append(("transfer_similar", transfer_detector(cfg, window, step),
                     {"source_events": events_from_jsonl(similar_source_path)}))
    arms += [("threshold", th, {}),
             ("source_free_forest", isolation(use_forest=True, use_novelty_gate=False), {}),
             ("novelty_gate", isolation(use_forest=False, use_novelty_gate=True), {}),
             ("source_free_source_features", SourceFeatureForest(n_estimators=int(sf_cfg["n_estimators"]),
                                                                 window_size=window, step_size=step,
                                                                 random_state=seed, **split), bgl)]

    if clean_window_certificate is not None:
        require_clean_window_certificate(Path(clean_window_certificate))

    results = {}
    seconds: Dict[str, Dict[str, float]] = {}
    for name, det, fit_kwargs in arms:
        start = time.perf_counter()
        det.fit(events, **fit_kwargs)
        fitted = time.perf_counter()
        results[name] = det.predict(events)
        seconds[name] = {"fit": fitted - start, "predict": time.perf_counter() - fitted}

    # All arms score one shared window grid; label sanity then runs once.
    first = next(iter(results.values()))
    for arm, res in results.items():
        same_grid = np.array_equal(res.y_true, first.y_true) and np.array_equal(
            res.event_indices, first.event_indices
        )
        if not same_grid:
            raise RuntimeError(f"detector {arm!r} scored a different window grid from the other arms")
    label_stats = assert_eval_label_sanity(first.y_true, context="window_eval", **sanity_kw)

    eval_events = [e for e in events if e.split == "eval"]
    if not eval_events:
        raise ValueError("no evaluation events (split == 'eval') to score")

    # Fault category of every window on the shared grid, and the fault-free windows made only of
    # elasticity-window events.
    win_cats = window_fault_categories(eval_events, first.event_indices, window)
    chunks = [eval_events[max(0, end - window + 1) : end + 1] for end in first.event_indices]
    control_windows = np.array([all(e.meta.get("phase") == "control" for e in c) for c in chunks], dtype=bool)
    control_windows &= np.asarray(first.y_true) == 0
    # Windows holding a line of a new execution environment's start (Lambda's INIT_START record).
    cold_start_windows = np.array([any(e.message.startswith("INIT_START") for e in c) for c in chunks], dtype=bool)
    # Delay of the latency fault behind a window's faulty lines (None for every other window).
    window_strengths = [max((e.meta.get("strength_ms") or 0 for e in c if e.is_anomaly), default=0) or None
                        for c in chunks]
    window_end_ms = np.array([eval_events[end].timestamp_ms for end in first.event_indices], dtype=np.int64)

    summaries: Dict[str, dict] = {}
    detector_meta: Dict[str, dict] = {}
    for name, det in results.items():
        s = summarise_result(det.y_true, det.y_pred)
        s["detection_delay"] = delay_summary(segment_delays(det.y_true, det.y_pred, window_end_ms))
        s["detector"] = name
        summaries[name] = s
        detector_meta[name] = {**(det.meta or {}), "seconds": seconds[name]}

    processed_dir.mkdir(parents=True, exist_ok=True)
    # Every fitted detector, for scoring other logs later (scripts/scoring/demo_detect.py).
    models_dir = processed_dir / "models"
    models_dir.mkdir(exist_ok=True)
    models = {}
    for name, det, _ in arms:
        models[name] = f"models/{name}.joblib"
        joblib.dump(det, processed_dir / models[name])

    # Baseline F1 (and MCC) minus each source-free detector's; "f1_source_features" is the BGL-trained
    # baseline minus the Isolation Forest on its own feature space (the feature-space ablation).
    forfeiture: Dict[str, float] = {}
    for baseline in BASELINE_ARMS:
        if baseline in summaries:
            for metric in ("f1", "mcc"):
                for source_free in SOURCE_FREE_ARMS:
                    forfeiture[f"{metric}:{baseline}-{source_free}"] = float(
                        summaries[baseline][metric] - summaries[source_free][metric])
    for metric in ("f1", "mcc"):
        forfeiture[f"{metric}:transfer-source_free_source_features"] = float(
            summaries["transfer"][metric] - summaries["source_free_source_features"][metric])

    md_path = processed_dir / "summary.txt"
    md_path.write_text(_render_summary(summaries, forfeiture, cfg), encoding="utf-8")

    # Per-window labels, fault categories and every detector's alarms on the shared grid.
    preds_path = processed_dir / "window_predictions.json"
    preds_path.write_text(
        json.dumps(
            {
                "event_indices": np.asarray(first.event_indices, dtype=int).tolist(),
                "y_true": np.asarray(first.y_true, dtype=int).tolist(),
                "window_categories": [str(c) for c in win_cats],
                "control_windows": control_windows.tolist(),
                "cold_start_windows": cold_start_windows.tolist(),
                "window_strengths_ms": window_strengths,
                "window_end_ms": window_end_ms.tolist(),
                "y_pred": {name: np.asarray(det.y_pred, dtype=int).tolist() for name, det in results.items()},
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # Model paths are relative to processed_dir, so a run scored elsewhere stays readable.
    payload = {
        "summaries": summaries,
        "label_stats": label_stats,
        "forfeiture": forfeiture,
        "config": cfg,
        "lexical_keyword_groups": KEYWORD_GROUPS,
        "detector_meta": detector_meta,
        "models": models,
    }
    (processed_dir / "results.json").write_text(
        json.dumps(payload, indent=2, default=str), encoding="utf-8"
    )
    return payload


def _render_summary(summaries: Dict[str, dict], forfeiture: Dict[str, float], cfg: dict) -> str:
    fcfg = cfg["features"]
    dcfg = cfg["detectors"]
    lines = [
        "# Experiment summary",
        "",
        f"- Seed {cfg['seed']}; windows of {fcfg['window_size']} lines, step {fcfg['step_size']}.",
        f"- The fault-free window is split in time: the later {dcfg['calib_share']} of its lines set every "
        f"alarm threshold at a {dcfg['calib_fpr']} false-alarm target; the earlier lines train.",
        "",
        "An undefined value prints as nan.",
        "",
        "| Detector | Precision | Recall | F1 | MCC | False-alarm rate | Segments detected | Median delay (s) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, s in summaries.items():
        d = s["detection_delay"]
        lines.append(
            f"| {ARM_ROLES[name]} | {s['precision']:.4f} | {s['recall']:.4f} | {s['f1']:.4f} | "
            f"{s['mcc']:.4f} | {s['false_alarm_rate']:.4f} | {d['n_detected_segments']} of {d['n_segments']} | "
            f"{'nan' if d['median_delay_seconds'] is None else format(d['median_delay_seconds'], '.1f')} |"
        )
    lines += ["", "## Forfeiture (baseline minus source-free)", ""]
    for key, value in forfeiture.items():
        metric, pair = key.split(":")
        baseline, source_free = pair.split("-")
        lines.append(f"- {metric.upper()}, {ARM_ROLES[baseline]} minus {ARM_ROLES[source_free]}: {value:.4f}")
    lines += ["", "results.json also holds the detector settings and the configuration.", ""]
    return "\n".join(lines)
