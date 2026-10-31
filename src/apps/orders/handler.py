"""Orders API Lambda: prices orders against an in-memory product catalogue and stores them in DynamoDB.

The catalogue is built once per execution environment; a memory setting below its working set fails at start-up.
"""

from __future__ import annotations

import json
import logging
import os
import time
import uuid
from decimal import Decimal
from typing import Any

import boto3
from botocore.exceptions import ClientError

TABLE_NAME = os.environ["TABLE_NAME"]
CATALOGUE_SIZE = int(os.environ["REFERENCE_DATA_SIZE"])
# Milliseconds to wait before handling a request: 0 when deployed, set only by the latency fault.
INJECTED_DELAY_MS = int(os.environ["INJECTED_DELAY_MS"])

logger = logging.getLogger()
logger.setLevel(os.environ["LOG_LEVEL"])
for library in ("boto3", "botocore", "urllib3"):
    logging.getLogger(library).setLevel(logging.WARNING)

# sku -> (product name, unit price in cents)
CATALOGUE = {f"SKU-{i:06d}": (f"product {i}", 100 + (i * 37) % 9900) for i in range(CATALOGUE_SIZE)}
DYNAMODB = boto3.client("dynamodb")


def _log(level: int, event: str, message: str) -> None:
    logger.log(level, json.dumps({"event": event, "message": message}))


def _response(status: int, body: dict[str, Any]) -> dict[str, Any]:
    return {"statusCode": status, "headers": {"Content-Type": "application/json"}, "body": json.dumps(body)}


def _route(event: dict[str, Any]) -> tuple[str, str]:
    return (event.get("httpMethod") or "").upper(), event.get("path") or "/"


def _create_order(body: dict[str, Any]) -> dict[str, Any]:
    sku, quantity = str(body.get("sku", "")), int(body.get("quantity", 1))
    if sku not in CATALOGUE:
        _log(logging.WARNING, "unknown_sku", f"sku {sku} is not in the catalogue")
        return _response(400, {"error": "unknown_sku"})
    name, cents = CATALOGUE[sku]
    order_id = str(uuid.uuid4())
    total = Decimal(cents * quantity) / 100
    DYNAMODB.put_item(
        TableName=TABLE_NAME,
        Item={
            "order_id": {"S": order_id},
            "sku": {"S": sku},
            "quantity": {"N": str(quantity)},
            "total": {"N": str(total)},
            "customer": {"S": str(body.get("customer", "anonymous"))},
            "status": {"S": "created"},
        },
    )
    _log(logging.INFO, "order_created", f"order {order_id}: {quantity} x {name}, total {total}")
    return _response(201, {"order_id": order_id, "total": str(total)})


def _get_order(order_id: str) -> dict[str, Any]:
    item = DYNAMODB.get_item(TableName=TABLE_NAME, Key={"order_id": {"S": order_id}}).get("Item")
    if not item:
        _log(logging.WARNING, "order_not_found", f"order {order_id} not found")
        return _response(404, {"error": "not_found"})
    _log(logging.INFO, "order_fetched", f"order {order_id} fetched with status {item['status']['S']}")
    return _response(200, {key: next(iter(value.values())) for key, value in item.items()})


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    method, path = _route(event)
    _log(logging.INFO, "request_received", f"{method} {path}")
    time.sleep(INJECTED_DELAY_MS / 1000)
    try:
        if method == "POST" and path.rstrip("/").endswith("/orders"):
            return _create_order(json.loads(event.get("body") or "{}"))
        order_id = (event.get("pathParameters") or {}).get("order_id")
        if method == "GET" and order_id:
            return _get_order(order_id)
    except ClientError as exc:
        error = exc.response.get("Error", {})
        _log(logging.ERROR, "dynamodb_error", f"{error.get('Code')}: {error.get('Message')}")
        return _response(500, {"error": error.get("Code")})
    _log(logging.WARNING, "route_not_found", f"no route for {method} {path}")
    return _response(404, {"error": "route_not_found"})
