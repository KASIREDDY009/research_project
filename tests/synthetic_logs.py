"""Synthetic CloudWatch-like logs for the unit tests."""

from __future__ import annotations

import json
import random
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from sflad.data.event_io import events_to_jsonl
from sflad.data.schema import FaultCategory, LogEvent

BURST_END_PROB = 0.3
ELASTICITY_TEMPLATE_PROB = 0.4
MS_PER_DAY = 86_400_000


# Template families that look like Lambda / API GW / DynamoDB / platform events.
NORMAL_TEMPLATES = [
    "START RequestId: {req} Version: $LATEST",
    "END RequestId: {req}",
    "REPORT RequestId: {req} Duration: {dur} ms Billed Duration: {bill} ms Memory Size: {mem} MB Max Memory Used: {used} MB",
    "INFO handler invoked path=/orders method=GET requestId={req}",
    "INFO fetched item from DynamoDB table=Orders id={item} latencyMs={lat}",
    "INFO wrote item to DynamoDB table=Orders id={item}",
    "INFO request status=200 path=/orders requestId={req}",
    "INFO cold start complete initDuration={init} ms",
    "INFO concurrency scale event reserved=0 provisioned=0",
    "INFO health check ok",
]

ELASTICITY_TEMPLATES = [
    "INFO Concurrent executions rising count={n}",
    "INFO Lambda scaling event capacity={n}",
    "INFO burst traffic detected rps={n}",
    "INFO provisioned concurrency warm-up count={n}",
]

SOURCE_EXTRA_TEMPLATES = [
    # Source-system phrasing that differs from the target templates.
    "INFO svc=orders-api action=get status=ok rid={req}",
    "INFO db.query table=orders elapsed={lat}ms",
    "WARN retry attempt={n} rid={req}",
    "INFO job completed jobId={item} duration={dur}ms",
]


def _rid(ids: random.Random) -> str:
    return str(uuid.UUID(int=ids.getrandbits(128), version=4))


def _fill(template: str, rng: random.Random, ids: random.Random) -> tuple[str, str]:
    req = _rid(ids)
    msg = template.format(
        req=req,
        dur=rng.randint(5, 400),
        bill=rng.randint(100, 500),
        mem=rng.choice([128, 256, 512, 1024]),
        used=rng.randint(40, 200),
        item=rng.randint(1, 9999),
        lat=rng.randint(1, 80),
        init=rng.randint(50, 900),
        n=rng.randint(2, 50),
    )
    return msg, req


class SyntheticLogGenerator:
    """Generate chronological CloudWatch-like events for target and source corpora."""

    def __init__(
        self,
        seed: int = 42,
        services: Optional[Sequence[str]] = None,
        base_rate_hz: float = 2.0,
        elasticity_burst_prob: float = 0.05,
        elasticity_burst_mult: float = 5.0,
        start_ts_ms: int = 1_700_000_000_000,
    ) -> None:
        self.rng = random.Random(seed)
        # Request ids come from their own seeded stream, so they are reproducible
        # without shifting the draws that shape the traffic.
        self.ids = random.Random(f"request-ids-{seed}")
        self.services = list(services or ["handler", "dynamodb", "cloudwatch"])
        self.base_rate_hz = base_rate_hz
        self.elasticity_burst_prob = elasticity_burst_prob
        self.elasticity_burst_mult = elasticity_burst_mult
        self.start_ts_ms = start_ts_ms

    def _next_delta_ms(self, burst: bool) -> int:
        rate = self.base_rate_hz * (self.elasticity_burst_mult if burst else 1.0)
        gap = self.rng.expovariate(max(rate, 0.1))
        return max(1, int(gap * 1000))

    def generate_target(
        self,
        n_events: int,
        train_frac: float = 0.5,
    ) -> List[LogEvent]:
        events: List[LogEvent] = []
        ts = self.start_ts_ms
        train_cut = int(n_events * train_frac)
        burst = False
        for i in range(n_events):
            if self.rng.random() < self.elasticity_burst_prob:
                burst = True
            elif self.rng.random() < BURST_END_PROB:
                burst = False

            templates = ELASTICITY_TEMPLATES if burst and self.rng.random() < ELASTICITY_TEMPLATE_PROB else NORMAL_TEMPLATES
            tmpl = self.rng.choice(templates)
            message, req = _fill(tmpl, self.rng, self.ids)
            service = self.rng.choice(self.services)
            split = "train" if i < train_cut else "eval"
            events.append(
                LogEvent(
                    timestamp_ms=ts,
                    message=message,
                    request_id=req,
                    meta={"service": service},
                    level="INFO" if "WARN" not in message else "WARN",
                    is_anomaly=False,
                    fault_category=FaultCategory.NONE.value,
                    split=split,
                )
            )
            ts += self._next_delta_ms(burst)
        return events

    def generate_source(self, n_events: int, anomaly_rate: float = 0.12) -> List[LogEvent]:
        """Labelled synthetic source corpus for the baseline tests."""
        from synthetic_faults import FaultInjector

        base: List[LogEvent] = []
        ts = self.start_ts_ms - MS_PER_DAY
        for _ in range(n_events):
            tmpl = self.rng.choice(NORMAL_TEMPLATES + SOURCE_EXTRA_TEMPLATES)
            message, req = _fill(tmpl, self.rng, self.ids)
            base.append(
                LogEvent(
                    timestamp_ms=ts,
                    message=message,
                    request_id=req,
                    meta={"service": self.rng.choice(self.services)},
                    level="INFO",
                    is_anomaly=False,
                    fault_category=FaultCategory.NONE.value,
                    split="source",
                    log_group="/synthetic/source-system",
                )
            )
            ts += self._next_delta_ms(False)

        injector = FaultInjector(seed=self.rng.randint(0, 10_000))
        # Gap > typical window_size so windows are not all-positive.
        return injector.inject(
            base,
            fault_rate=anomaly_rate,
            inject_after_frac=0.0,
            categories=["permission", "config", "timeout", "resource"],
            min_fault_gap_events=max(30, int(1.5 / max(anomaly_rate, 0.01))),
            fault_burst_size=2,
        )


def generate_dataset(cfg: Dict[str, Any], out_dir: Path) -> Dict[str, Path]:
    """Generate a synthetic target (with injected faults) and a labelled source corpus for the tests."""
    from synthetic_faults import FaultInjector

    seed = int(cfg["seed"])
    gcfg = cfg["generator"]
    icfg = cfg["injector"]

    gen = SyntheticLogGenerator(
        seed=seed,
        services=gcfg["services"],
        base_rate_hz=float(gcfg["base_rate_hz"]),
        elasticity_burst_prob=float(gcfg["elasticity_burst_prob"]),
        elasticity_burst_mult=float(gcfg["elasticity_burst_mult"]),
    )

    train_frac = float(cfg["train_frac"])
    target_normal = gen.generate_target(
        n_events=int(gcfg["n_normal_events"]),
        train_frac=train_frac,
    )
    injector = FaultInjector(seed=seed + 7)
    fault_rate = float(icfg["fault_rate"])
    categories = list(icfg["categories"])
    target = injector.inject(
        target_normal,
        fault_rate=fault_rate,
        inject_after_frac=float(icfg["inject_after_frac"]),
        categories=categories,
        min_fault_gap_events=int(icfg["min_fault_gap_events"]),
        fault_burst_size=int(icfg["fault_burst_size"]),
    )

    source = gen.generate_source(
        n_events=int(gcfg["n_source_events"]),
        anomaly_rate=float(gcfg["source_anomaly_rate"]),
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    target_path = out_dir / "events.jsonl"
    source_path = out_dir / "source_events.jsonl"
    meta_path = out_dir / "meta.json"

    events_to_jsonl(target, target_path)
    events_to_jsonl(source, source_path)

    n_anom = sum(1 for e in target if e.is_anomaly)
    meta = {
        "seed": seed,
        "n_target": len(target),
        "n_target_anomalies": n_anom,
        "n_source": len(source),
        "n_source_anomalies": sum(1 for e in source if e.is_anomaly),
        "train_frac": train_frac,
        "fault_rate_requested": fault_rate,
        "categories": categories,
    }
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return {"events": target_path, "source_events": source_path, "meta": meta_path}
