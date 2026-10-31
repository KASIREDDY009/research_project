#!/usr/bin/env python3
"""Build a labelled-source corpus for a labelled-source baseline, with each line's own severity level.

BGL: the LogHub BGL_2k sample. OpenStack: the labelled LogHub OpenStack set (openstack_normal1.log and
openstack_abnormal.log with anomaly_labels.txt), the OpenStack set of the published ELFA-Log results.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from sflad.data.event_io import events_to_jsonl  # noqa: E402
from sflad.data.loghub import load_bgl, load_openstack  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("corpus", choices=["BGL", "OpenStack"])
    p.add_argument("--input", type=Path, required=True,
                   help="BGL: the BGL_2k.log file; OpenStack: the folder holding the three OpenStack files")
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args(argv)
    if a.corpus == "BGL":
        events = load_bgl(a.input, split="source")
    else:
        pins = yaml.safe_load((ROOT / "configs" / "corpus.yaml").read_text())["openstack_source"]["sha256"]
        for name in ("openstack_normal1.log", "openstack_abnormal.log", "anomaly_labels.txt"):
            if sha256(a.input / name) != pins[name]:
                raise SystemExit(f"{name} differs from its pin in configs/corpus.yaml")
        abnormal = a.input / "openstack_abnormal.log"
        events = load_openstack([a.input / "openstack_normal1.log", abnormal], a.input / "anomaly_labels.txt",
                                split="source", anomalous_files=[abnormal])
    a.out.parent.mkdir(parents=True, exist_ok=True)
    events_to_jsonl(events, a.out)
    digest = sha256(a.out)
    print(f"{a.out.name}: events={len(events)} anomalies={sum(e.is_anomaly for e in events)} sha256={digest}")
    if a.corpus == "OpenStack" and digest != pins["source_events.jsonl"]:
        raise SystemExit("the rebuilt source differs from its pin in configs/corpus.yaml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
