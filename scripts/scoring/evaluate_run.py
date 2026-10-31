#!/usr/bin/env python3
"""Every detector on one application's run export.

Reads RUN/raw (events.jsonl, run.json, export.json), certifies the training window from its labels
and writes RUN/processed; RUN/raw is never written to. The BGL-trained and OpenStack-trained baselines'
labelled sources are pinned in configs/corpus.yaml; scoring stops when one is missing or its sha256
differs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from importlib.metadata import version
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from sflad.data.event_io import events_from_jsonl  # noqa: E402
from sflad.pipeline.clean_window import write_clean_window_certificate  # noqa: E402
from sflad.pipeline.train_eval import load_config, run_experiment  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("run", type=Path)
    p.add_argument("--similar-source", type=Path,
                   help="labelled events.jsonl of the other application's evaluation run (the similar-application baseline's source)")
    p.add_argument("--config", type=Path, default=ROOT / "configs" / "default.yaml",
                   help="detector and analysis settings (default: configs/default.yaml)")
    a = p.parse_args(argv)
    raw = a.run / "raw"
    cfg = load_config(a.config)
    corpus = yaml.safe_load((ROOT / "configs" / "corpus.yaml").read_text())
    sources = {}
    for key in ("baseline_source", "openstack_source"):
        path = ROOT / corpus[key]["paths"]["source_events_jsonl"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != corpus[key]["sha256"]["source_events.jsonl"]:
            raise SystemExit(f"labelled source {path.relative_to(ROOT)} has sha256 {digest}, not the pinned one")
        sources[key] = path

    run_meta = json.loads((raw / "run.json").read_text())
    train = [e for e in events_from_jsonl(raw / "events.jsonl") if e.split == "train"]
    certificate = a.run / "processed" / "clean_window_certificate.json"
    write_clean_window_certificate(
        certificate,
        train_start=str(run_meta["times"]["start"]),
        train_end=str(run_meta["times"]["train_end"]),
        n_events=len(train),
        n_failed_call_lines=sum(1 for e in train if e.is_anomaly),
        seed=int(cfg["seed"]),
        extra={"app": run_meta["app"]},
    )
    payload = run_experiment(
        cfg, raw / "events.jsonl", sources["baseline_source"], a.run / "processed",
        clean_window_certificate=certificate,
        similar_source_path=a.similar_source,
        openstack_source_path=sources["openstack_source"],
    )
    payload["run"] = json.loads((raw / "export.json").read_text())
    payload["environment"] = {"python": platform.python_version(),
                              **{pkg: version(pkg) for pkg in ("numpy", "scipy", "scikit-learn", "pandas", "torch")}}
    if a.similar_source:
        payload["similar_source_sha256"] = hashlib.sha256(a.similar_source.read_bytes()).hexdigest()
    (a.run / "processed" / "results.json").write_text(json.dumps(payload, indent=2, default=str))
    for category, c in sorted(payload["run"]["episodes"].items()):
        print(f"{category}: {c['episodes']} episodes, {c['silent']} silent, {c['partial']} partly silent")
    for name, s in payload["summaries"].items():
        print(f"{name:20s} P={s['precision']:.3f} R={s['recall']:.3f} F1={s['f1']:.3f} MCC={s['mcc']:.3f} "
              f"FAR={s['false_alarm_rate']:.3f}")
    print(f"F1 forfeiture (BGL-trained baseline minus source-free Isolation Forest): "
          f"{payload['forfeiture']['f1:transfer-source_free']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
