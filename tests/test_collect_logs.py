from __future__ import annotations

import pytest

from sflad.aws.collect_logs import IncompleteExportError, export_events, label_events, parse_line

A = "11111111-1111-4111-8111-111111111111"
B = "22222222-2222-4222-8222-222222222222"
TIMES = {"start": 0, "train_end": 5, "control_start": 100, "end": 200}


def _line(ts, message, stream="s1"):
    return {"timestamp": ts, "message": message + "\n", "logStreamName": stream}


LIMIT = 3000


def _rec(rid, phase, status=201, function_error=None, category=None, episode=None, latency=200, content_ok=True):
    return {"request_id": rid, "phase": phase, "status_code": status, "function_error": function_error,
            "category": category, "episode": episode, "start_ms": 0, "end_ms": latency,
            "content_ok": content_ok and function_error is None and (status or 0) < 500}


def test_parse_line_reads_runtime_and_platform_lines():
    assert parse_line(f"[ERROR]\t2026-09-23T19:41:54.567Z\t{A}\tstorage failure") == ("ERROR", A, "storage failure")
    assert parse_line(f"REPORT RequestId: {A}\tDuration: 9 ms") == ("UNKNOWN", A, f"REPORT RequestId: {A}\tDuration: 9 ms")
    assert parse_line("INIT_START Runtime Version: python:3.12") == ("UNKNOWN", "", "INIT_START Runtime Version: python:3.12")


def _export():
    return [
        _line(1, "INIT_START Runtime Version: python:3.12"),
        _line(2, f"START RequestId: {A} Version: $LATEST"),
        _line(3, f"[INFO]\tts\t{A}\trequest received"),
        _line(4, f"REPORT RequestId: {A}\tDuration: 5 ms\tInit Duration: 700 ms"),
        _line(10, f"START RequestId: {B} Version: $LATEST", "s2"),
        _line(11, f"[ERROR]\tts\t{B}\tAccessDeniedException", "s2"),
        _line(12, f"REPORT RequestId: {B}\tDuration: 9 ms", "s2"),
    ]


def test_lines_take_the_outcome_of_their_invocation_and_init_lines_the_next_request():
    records = [_rec(A, "train"), _rec(B, "fault", status=500, category="permission", episode="permission-00")]
    events = label_events(_export(), records, "/aws/lambda/x", times=TIMES, episodes=[], slow_limit_ms=LIMIT)
    assert [e.request_id for e in events] == [A, A, A, A, B, B, B]
    assert [e.is_anomaly for e in events] == [False] * 4 + [True] * 3
    assert {e.fault_category for e in events if e.is_anomaly} == {"permission"}
    assert [e.split for e in events] == ["train"] * 4 + ["eval"] * 3
    assert [e.level for e in events][2] == "INFO" and events[5].level == "ERROR"


def test_a_timeout_without_an_error_line_is_still_anomalous():
    records = [_rec(A, "train"), _rec(B, "fault", status=None, function_error="Unhandled", category="timeout")]
    events = label_events(_export(), records, "g", times=TIMES, episodes=[], slow_limit_ms=LIMIT)
    assert all(e.is_anomaly for e in events if e.request_id == B)


def test_a_slow_call_or_one_without_the_expected_content_is_anomalous_and_a_fast_correct_one_is_not():
    for b, anomalous in ((_rec(B, "fault", category="latency", latency=LIMIT + 1), True),
                         (_rec(B, "fault", category="latency", latency=LIMIT), False),
                         (_rec(B, "gap", content_ok=False), True)):
        events = label_events(_export(), [_rec(A, "train"), b], "g", times=TIMES, episodes=[], slow_limit_ms=LIMIT)
        assert all(e.is_anomaly == anomalous for e in events if e.request_id == B)
        assert not any(e.is_anomaly for e in events if e.request_id == A)


def test_an_unrecorded_request_id_or_a_missing_report_stops_the_labelling():
    with pytest.raises(ValueError, match="not recorded"):
        label_events(_export(), [_rec(A, "train")], "g", times=TIMES, episodes=[], slow_limit_ms=LIMIT)
    with pytest.raises(IncompleteExportError):
        label_events(_export()[:-1], [_rec(A, "train"), _rec(B, "fault")], "g", times=TIMES, episodes=[], slow_limit_ms=LIMIT)


def test_export_follows_empty_pages_until_the_token_ends(monkeypatch):
    import boto3
    from botocore.stub import Stubber

    from sflad.aws import collect_logs

    client = boto3.client("logs", region_name="eu-west-1", aws_access_key_id="k", aws_secret_access_key="s")
    stub = Stubber(client)
    ev = [{"timestamp": i, "message": f"m{i}", "logStreamName": "s", "eventId": str(i), "ingestionTime": i}
          for i in range(3)]
    base = {"logGroupName": "g", "startTime": 0, "endTime": 9}
    stub.add_response("filter_log_events", {"events": ev[:1], "nextToken": "a"}, base)
    stub.add_response("filter_log_events", {"events": [], "nextToken": "b"}, {**base, "nextToken": "a"})
    stub.add_response("filter_log_events", {"events": ev[1:]}, {**base, "nextToken": "b"})
    monkeypatch.setattr(collect_logs, "make_client", lambda service, region=None: client)
    with stub:
        events = export_events("g", 0, 9)
    assert [e["message"] for e in events] == ["m0", "m1", "m2"]
    stub.assert_no_pending_responses()


def test_a_line_without_any_request_id_is_negative_marked_and_placed_by_the_recorded_intervals():
    orphan = _line(40, "INIT_REPORT Init Duration: 10002.29 ms\tPhase: init\tStatus: timeout", "s9")
    records = [_rec(A, "train"), _rec(B, "fault", status=500, category="config", episode="config-00")]
    episodes = [{"inject_ms": 30, "restored_ms": 50}]
    events = label_events(_export() + [orphan], records, "g", times=TIMES, episodes=episodes, slow_limit_ms=LIMIT)
    line = next(e for e in events if e.timestamp_ms == 40)
    assert line.request_id == "" and not line.is_anomaly and line.split == "eval"
    assert line.meta == {"phase": "fault", "episode": None, "strength_ms": None, "orphan": True}
    assert not any(e.meta["orphan"] for e in events if e.timestamp_ms != 40)
