from __future__ import annotations

import io
import json
import random

from sflad.aws.workload import create_burst, failed, normal_traffic

APP = {"function_name": "fn", "resource": "orders", "table_key": "order_id", "environment": {"REFERENCE_DATA_SIZE": "100"}}


class FakeLambda:
    class exceptions:
        class TooManyRequestsException(Exception):
            pass

        class KMSAccessDeniedException(Exception):
            pass

    def __init__(self):
        self.events, self.n = [], 0

    def invoke(self, FunctionName, Payload):
        event = json.loads(Payload)
        self.events.append(event)
        self.n += 1
        if event["httpMethod"] == "POST":
            body = {"statusCode": 201, "body": json.dumps({"order_id": f"o{self.n}"})}
        elif event["pathParameters"]["order_id"].startswith("missing-"):
            body = {"statusCode": 404, "body": "{}"}
        else:
            body = {"statusCode": 200, "body": "{}"}
        return {"ResponseMetadata": {"RequestId": f"r{self.n}"}, "Payload": io.BytesIO(json.dumps(body).encode())}


def test_failure_is_a_function_error_or_a_server_error_only():
    base = {"function_error": None, "status_code": 201}
    assert not failed(base) and not failed({**base, "status_code": 404})
    assert failed({**base, "status_code": 500}) and failed({"function_error": "Unhandled", "status_code": None})


def test_normal_traffic_reads_back_what_it_created_and_records_every_call(monkeypatch):
    monkeypatch.setattr("sflad.aws.workload.time.sleep", lambda s: None)
    lam = FakeLambda()
    records = normal_traffic(lam, "orders", APP, 40, random.Random(1), 0.0, {"phase": "train"})
    posts = [r for r in records if r["method"] == "POST"]
    assert len(posts) == 40 and all(r["phase"] == "train" for r in records)
    reads = [e for e in lam.events if e["httpMethod"] == "GET"]
    assert {e["pathParameters"]["order_id"] for e in reads if not e["pathParameters"]["order_id"].startswith("missing-")} \
        == {r["created"] for r in posts}
    assert not any(failed(r) for r in records)
    assert len({r["request_id"] for r in records}) == len(records)


def test_a_concurrent_burst_makes_k_create_calls():
    records = create_burst(FakeLambda(), "orders", APP, 5, random.Random(2), {"phase": "control"}, concurrent=True)
    assert len(records) == 5 and all(r["method"] == "POST" and r["phase"] == "control" for r in records)


def test_a_refused_call_is_sent_again_and_recorded_once(monkeypatch):
    import pytest

    from sflad.aws.workload import invoke

    monkeypatch.setattr("sflad.aws.workload.time.sleep", lambda s: None)
    lam = FakeLambda()
    real, refusals = lam.invoke, [FakeLambda.exceptions.KMSAccessDeniedException,
                                  FakeLambda.exceptions.TooManyRequestsException]

    def flaky(**kw):
        if refusals:
            raise refusals.pop()()
        return real(**kw)

    lam.invoke = flaky
    record = invoke(lam, APP, "POST", {"phase": "train"}, 201, body={"sku": "SKU-000001"})
    assert record["status_code"] == 201 and record["request_id"] == "r1" and record["resent"] == 2

    lam.invoke = lambda **kw: {"ResponseMetadata": {"RequestId": "x"}, "Payload": io.BytesIO(b"not json")}
    with pytest.raises(ValueError, match="neither a function error nor a status code"):
        invoke(lam, APP, "POST", {"phase": "train"}, 201, body={})
