"""Log event schema shared by the exported runs, the public corpora and the synthetic test logs."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class FaultCategory(str, Enum):
    """The five injected fault categories, none, and the category of a faulty call outside a fault."""

    NONE = "none"
    PERMISSION = "permission"
    CONFIG = "config"
    TIMEOUT = "timeout"
    RESOURCE = "resource"
    LATENCY = "latency"
    UNATTRIBUTED = "unattributed"  # a faulty call outside every fault episode


def normalize_fault_category(label: str) -> str:
    """The category code of a label (case and surrounding spaces ignored)."""
    key = (label or "").strip().lower()
    if key in {c.value for c in FaultCategory}:
        return key
    raise ValueError(f"Unknown fault category: {label!r}")


@dataclass(frozen=True)
class LogEvent:
    """One log line with its label."""

    timestamp_ms: int
    message: str
    log_group: str = ""
    log_stream: str = ""
    request_id: str = ""
    level: str = "INFO"
    is_anomaly: bool = False
    fault_category: str = FaultCategory.NONE.value
    split: str = "train"  # train | eval | source
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "LogEvent":
        known = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        payload = {k: v for k, v in d.items() if k in known}
        return cls(**payload)
