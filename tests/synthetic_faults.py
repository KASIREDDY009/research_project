"""Synthetic faults for the unit-test logs.

Categories: permission, config, timeout, resource.
Faults are injected only after inject_after_frac, so the training window stays fault-free.
"""

from __future__ import annotations

import random
import uuid
from dataclasses import replace
from typing import List, Sequence

from sflad.data.schema import FaultCategory, LogEvent

FAULT_MESSAGES = {
    FaultCategory.PERMISSION.value: [
        "ERROR AccessDeniedException: User is not authorized to perform: dynamodb:GetItem on resource: table/Orders requestId={req}",
        "ERROR [ERROR] Forbidden: access to path=/admin returned 403 requestId={req}",
        "ERROR Cognito UnauthorizedException: Invalid token requestId={req}",
    ],
    FaultCategory.CONFIG.value: [
        "ERROR ResourceNotFoundException: Requested resource not found: table/Orderz (misconfigured name) requestId={req}",
        "ERROR ConfigError: Missing environment variable ORDERS_TABLE requestId={req}",
        "ERROR InvalidParameter: Lambda timeout set below cold-start initDuration requestId={req}",
    ],
    FaultCategory.TIMEOUT.value: [
        "ERROR Task timed out after 3.00 seconds requestId={req}",
        "ERROR [ERROR] TimeoutError: Downstream DynamoDB call exceeded 2000ms requestId={req}",
        "ERROR Endpoint request timed out endpoint=dynamodb requestId={req}",
    ],
    FaultCategory.RESOURCE.value: [
        "ERROR Runtime.OutOfMemory: Memory limit of 128 MB exceeded requestId={req}",
        "ERROR ThrottlingException: Rate exceeded for dynamodb:PutItem requestId={req}",
        "ERROR ConcurrentInvocationLimitExceeded: Account concurrency limit reached requestId={req}",
    ],
}


class FaultInjector:
    def __init__(self, seed: int = 42) -> None:
        self.rng = random.Random(seed)
        # Identifiers come from their own seeded stream, so they are reproducible
        # without shifting the draws that place faults.
        self.ids = random.Random(f"fault-ids-{seed}")

    def inject(
        self,
        events: Sequence[LogEvent],
        *,
        fault_rate: float,
        inject_after_frac: float,
        categories: Sequence[str],
        min_fault_gap_events: int,
        fault_burst_size: int,
    ) -> List[LogEvent]:
        if not events:
            return []
        cats = list(categories)
        n = len(events)
        start = int(n * inject_after_frac)
        region_len = max(1, n - start)
        n_faults = max(1, int(round(region_len * fault_rate))) if fault_rate > 0 else 0

        burst = max(1, int(fault_burst_size))
        candidates = list(range(start, max(start, n - burst + 1)))
        self.rng.shuffle(candidates)
        chosen_starts: List[int] = []
        for idx in candidates:
            if len(chosen_starts) >= n_faults:
                break
            if any(abs(idx - c) < min_fault_gap_events for c in chosen_starts):
                continue
            chosen_starts.append(idx)

        # Map every event index in each burst to the same category.
        anom_at: dict[int, str] = {}
        for start_idx in chosen_starts:
            cat = self.rng.choice(cats)
            for off in range(burst):
                anom_at[start_idx + off] = cat

        out: List[LogEvent] = []
        for i, ev in enumerate(events):
            if i not in anom_at:
                out.append(ev)
                continue
            cat = anom_at[i]
            tmpl = self.rng.choice(FAULT_MESSAGES[cat])
            req = ev.request_id or str(uuid.UUID(int=self.ids.getrandbits(128), version=4))
            msg = tmpl.format(req=req)
            out.append(
                replace(
                    ev,
                    message=msg,
                    level="ERROR",
                    is_anomaly=True,
                    fault_category=cat,
                )
            )
        return out
