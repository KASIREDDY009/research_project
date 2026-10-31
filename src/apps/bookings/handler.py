"""Bookings API Lambda: reserves venue time slots against an in-memory venue calendar in DynamoDB.

The calendar is built once per execution environment; a memory setting below its working set fails at start-up.
"""

from __future__ import annotations

import json
import logging
import os
import time
import uuid
from typing import Any

import boto3
from botocore.exceptions import ClientError

TABLE_NAME = os.environ["TABLE_NAME"]
VENUE_COUNT = int(os.environ["REFERENCE_DATA_SIZE"])
# Milliseconds to wait before handling a request: 0 when deployed, set only by the latency fault.
INJECTED_DELAY_MS = int(os.environ["INJECTED_DELAY_MS"])
SLOTS_PER_DAY = 12

logger = logging.getLogger()
logger.setLevel(os.environ["LOG_LEVEL"])
for library in ("boto3", "botocore", "urllib3"):
    logging.getLogger(library).setLevel(logging.WARNING)

# venue id -> (city, seats per slot)
CALENDAR = {f"V{v:06d}": (f"city-{v % 97}", 10 + v % 40) for v in range(VENUE_COUNT)}
DYNAMODB = boto3.client("dynamodb")


def _log(level: int, event: str, message: str) -> None:
    logger.log(level, json.dumps({"event": event, "message": message}))


def _response(status: int, body: dict[str, Any]) -> dict[str, Any]:
    return {"statusCode": status, "headers": {"Content-Type": "application/json"}, "body": json.dumps(body)}


def _route(event: dict[str, Any]) -> tuple[str, str]:
    return (event.get("httpMethod") or "").upper(), event.get("path") or "/"


def _reserve(body: dict[str, Any]) -> dict[str, Any]:
    venue, slot, guests = str(body.get("venue", "")), int(body.get("slot", -1)), int(body.get("guests", 1))
    if venue not in CALENDAR or not 0 <= slot < SLOTS_PER_DAY:
        _log(logging.WARNING, "slot_rejected", f"venue {venue} has no slot {slot}")
        return _response(400, {"error": "unknown_slot"})
    city, seats = CALENDAR[venue]
    if guests > seats:
        _log(logging.WARNING, "party_too_large", f"{guests} guests exceed {seats} seats at {venue}")
        return _response(409, {"error": "party_too_large"})
    booking_id = str(uuid.uuid4())
    DYNAMODB.put_item(
        TableName=TABLE_NAME,
        Item={
            "booking_id": {"S": booking_id},
            "venue": {"S": venue},
            "slot": {"N": str(slot)},
            "guests": {"N": str(guests)},
            "state": {"S": "confirmed"},
        },
    )
    _log(logging.INFO, "booking_confirmed", f"booking {booking_id}: {guests} guests at {venue} ({city}) slot {slot}")
    return _response(201, {"booking_id": booking_id})


def _lookup(booking_id: str) -> dict[str, Any]:
    item = DYNAMODB.get_item(TableName=TABLE_NAME, Key={"booking_id": {"S": booking_id}}).get("Item")
    if not item:
        _log(logging.WARNING, "booking_missing", f"no booking {booking_id}")
        return _response(404, {"error": "not_found"})
    _log(logging.INFO, "booking_found", f"booking {booking_id} is {item['state']['S']}")
    return _response(200, {key: next(iter(value.values())) for key, value in item.items()})


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    method, path = _route(event)
    _log(logging.INFO, "call_started", f"{method} {path}")
    time.sleep(INJECTED_DELAY_MS / 1000)
    try:
        if method == "POST" and path.rstrip("/").endswith("/bookings"):
            return _reserve(json.loads(event.get("body") or "{}"))
        booking_id = (event.get("pathParameters") or {}).get("booking_id")
        if method == "GET" and booking_id:
            return _lookup(booking_id)
    except ClientError as exc:
        error = exc.response.get("Error", {})
        _log(logging.ERROR, "storage_failure", f"{error.get('Code')}: {error.get('Message')}")
        return _response(500, {"error": error.get("Code")})
    _log(logging.WARNING, "unknown_route", f"no route for {method} {path}")
    return _response(404, {"error": "route_not_found"})
