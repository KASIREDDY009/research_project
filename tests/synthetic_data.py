"""Settings of the synthetic logs the unit tests generate."""
from __future__ import annotations

from pathlib import Path

import yaml


def synthetic_config(seed: int = 42) -> dict:
    cfg = yaml.safe_load((Path(__file__).with_name("synthetic.yaml")).read_text())
    return {"seed": seed, **cfg}
