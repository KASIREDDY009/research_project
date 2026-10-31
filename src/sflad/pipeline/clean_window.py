"""Clean-window certificate for the source-free detectors (training-window contamination check)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def write_clean_window_certificate(
    path: Path,
    *,
    train_start: str,
    train_end: str,
    n_events: int,
    n_failed_call_lines: int,
    seed: int,
    extra: dict[str, Any] | None = None,
) -> Path:
    if n_failed_call_lines != 0:
        raise ValueError(
            f"The training window holds {n_failed_call_lines} line(s) of failed calls"
        )
    payload = {
        "type": "clean_window_certificate",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "train_start": train_start,
        "train_end": train_end,
        "n_events": n_events,
        "n_failed_call_lines": n_failed_call_lines,
        "seed": seed,
        "status": "certified_clean",
    }
    if extra:
        payload["extra"] = extra
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def require_clean_window_certificate(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing clean-window certificate: {path}; the source-free detectors are not trained."
        )
    data = json.loads(path.read_text(encoding="utf-8"))
    if data["n_failed_call_lines"] != 0 or data["status"] != "certified_clean":
        raise ValueError(f"Clean-window certificate invalid: {path}")
    return data
