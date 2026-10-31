"""Drive an application through direct Lambda invocations and record every call.

Each record carries the invocation's AWS request id, which the function's CloudWatch lines
also carry, plus its outcome; ground truth is derived from these records, never from log text.
"""

from __future__ import annotations

import json
import random
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, List, Optional

OnRecord = Optional[Callable[[Dict[str, Any]], None]]

RESEND_ATTEMPTS = 10


def failed(record: Dict[str, Any]) -> bool:
    """The call failed when Lambda reports a function error or the app answers 5xx."""
    return record["function_error"] is not None or (record["status_code"] or 0) >= 500


def latency_ms(record: Dict[str, Any]) -> int:
    """The call's time from sending to the full answer, measured by this script."""
    return record["end_ms"] - record["start_ms"]


def fault_reasons(record: Dict[str, Any], slow_limit_ms: int | None) -> List[str]:
    """Why a call counts as faulty: it failed, it took longer than the run's slow limit (None before the
    limit is set, at the end of the training window), or its answer lacked the expected content."""
    reasons = []
    if failed(record):
        reasons.append("failed")
    if slow_limit_ms is not None and latency_ms(record) > slow_limit_ms:
        reasons.append("slow")
    if not failed(record) and not record["content_ok"]:
        reasons.append("incorrect")
    return reasons


def faulty(record: Dict[str, Any], slow_limit_ms: int | None) -> bool:
    """Impact rule: a call is faulty when it failed, was slow or answered without the expected content."""
    return bool(fault_reasons(record, slow_limit_ms))


def _create_body(app_name: str, reference_size: int, rng: random.Random) -> dict:
    if app_name == "orders":
        return {
            "sku": f"SKU-{rng.randrange(reference_size):06d}",
            "quantity": rng.randint(1, 5),
            "customer": f"customer-{rng.randrange(5000)}",
        }
    return {"venue": f"V{rng.randrange(reference_size):06d}", "slot": rng.randrange(12), "guests": rng.randint(1, 6)}


def invoke(lam, app: dict, method: str, labels: dict, expect: int, body: Optional[dict] = None,
           item_id: Optional[str] = None, on_record: OnRecord = None) -> Dict[str, Any]:
    """Call the function once; on_record receives the record as soon as the call returns.

    expect is the answer a correct call gives: 201 with the new item's id for a create, 200 with the
    asked item for a read of a created item, 404 for a read of an item that does not exist."""
    key = app["table_key"]
    event = {
        "httpMethod": method,
        "path": f"/{app['resource']}" + (f"/{item_id}" if item_id else ""),
        "pathParameters": {key: item_id} if item_id else None,
        "body": json.dumps(body) if body is not None else None,
    }
    # Lambda refuses these calls before the function runs, so they leave no log line.
    refused = (lam.exceptions.TooManyRequestsException, lam.exceptions.KMSAccessDeniedException)
    for attempt in range(RESEND_ATTEMPTS):
        start = time.time()
        try:
            resp = lam.invoke(FunctionName=app["function_name"], Payload=json.dumps(event).encode())
            break
        except refused:
            time.sleep(min(2 ** attempt, 30))
    else:
        raise RuntimeError(f"{app['function_name']} refused the call on every attempt")
    raw = resp["Payload"].read()
    end = time.time()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        payload = None
    if resp.get("FunctionError") is None and not (isinstance(payload, dict) and isinstance(payload.get("statusCode"), int)):
        raise ValueError(f"{app['function_name']} answered with neither a function error nor a status code")
    payload = payload if isinstance(payload, dict) else {}
    status = payload.get("statusCode")
    try:
        answer = json.loads(payload.get("body") or "{}")
    except json.JSONDecodeError:
        answer = None
    answer = answer if isinstance(answer, dict) else {}
    item = answer.get(key) if status == 201 else None
    if expect == 201:
        content_ok = status == 201 and bool(item)
    elif expect == 200:
        content_ok = status == 200 and answer.get(key) == item_id
    else:
        content_ok = status == expect
    record = {
        "request_id": resp["ResponseMetadata"]["RequestId"],
        "method": method,
        "start_ms": int(start * 1000),
        "end_ms": int(end * 1000),
        "function_error": resp.get("FunctionError"),
        "status_code": payload.get("statusCode"),
        "error_type": payload.get("errorType"),
        "created": item,
        "expected_status": expect,
        "content_ok": content_ok,
        "resent": attempt,  # times the call was refused before it ran and sent again
        **labels,
    }
    if on_record is not None:
        on_record(record)
    return record


def normal_traffic(lam, app_name: str, app: dict, n: int, rng: random.Random, pause: float,
                   labels: dict, on_record: OnRecord = None) -> List[Dict[str, Any]]:
    """n cycles of create-then-read; one read in twenty asks for an item that does not exist (404)."""
    size = int(app["environment"]["REFERENCE_DATA_SIZE"])
    records = []
    for _ in range(n):
        created = invoke(lam, app, "POST", labels, 201, body=_create_body(app_name, size, rng),
                         on_record=on_record)
        records.append(created)
        if created["created"]:
            records.append(invoke(lam, app, "GET", labels, 200, item_id=created["created"],
                                  on_record=on_record))
        if rng.random() < 0.05:
            records.append(invoke(lam, app, "GET", labels, 404, item_id=f"missing-{rng.randrange(10**9)}",
                                  on_record=on_record))
        time.sleep(pause)
    return records


def create_burst(lam, app_name: str, app: dict, k: int, rng: random.Random, labels: dict,
                 concurrent: bool = False, on_record: OnRecord = None) -> List[Dict[str, Any]]:
    """k create calls, one after another or all at once (concurrent calls scale out new environments)."""
    size = int(app["environment"]["REFERENCE_DATA_SIZE"])
    bodies = [_create_body(app_name, size, rng) for _ in range(k)]

    def call(body):
        return invoke(lam, app, "POST", labels, 201, body=body, on_record=on_record)

    if not concurrent:
        return [call(b) for b in bodies]
    with ThreadPoolExecutor(max_workers=k) as pool:
        return list(pool.map(call, bodies))
