from __future__ import annotations

import io
import json

import pytest

from sflad.aws.evaluation_run import run_evaluation

ACCOUNT = "123456789012"
APP = {"function_name": "fn", "role_arn": f"arn:aws:iam::{ACCOUNT}:role/r", "logs_role_arn": f"arn:aws:iam::{ACCOUNT}:role/l", "table_name": "t",
       "table_key": "order_id", "resource": "orders", "timeout_seconds": 10, "memory_size": 512,
       "environment": {"TABLE_NAME": "t", "LOG_LEVEL": "INFO", "REFERENCE_DATA_SIZE": "100", "INJECTED_DELAY_MS": "0"}}
CFG = {"workload": {"train_cycles": 2, "train_sham_every_cycles": 2, "gap_cycles": 1, "fault_burst": 2,
                    "pause_seconds": 0},
       "faults": {"categories": ["config"], "injections_per_category": 1, "fault_timeout_seconds": 3,
                  "unreachable_endpoint": "https://10.255.255.1", "starved_memory_mb": 128,
                  "injected_delays_ms": [4000, 6000]},
       "labels": {"slow_margin_ms": 1000},
       "control": {"bursts": 1, "burst_concurrency": 2, "cycles_between_bursts": 1, "idle_seconds": 0}}
BASELINE = {"Environment": {"Variables": APP["environment"]}, "Timeout": 10, "MemorySize": 512, "Role": APP["role_arn"]}


class Config:
    class _Waiter:
        def wait(self, **kw):
            pass

    def __init__(self):
        self.updates = []

    def get_waiter(self, name):
        return self._Waiter()

    def update_function_configuration(self, FunctionName, **settings):
        self.updates.append(settings)


class Invoker:
    class exceptions:
        class TooManyRequestsException(Exception):
            pass

        class KMSAccessDeniedException(Exception):
            pass

    def __init__(self, fail_at):
        self.n, self.fail_at = 0, fail_at

    def invoke(self, FunctionName, Payload):
        self.n += 1
        if self.n == self.fail_at:
            raise ConnectionError("network gone")
        event = json.loads(Payload)
        item = (event.get("pathParameters") or {}).get("order_id")
        if event["httpMethod"] == "POST":
            body = {"statusCode": 201, "body": json.dumps({"order_id": f"o{self.n}"})}
        elif item.startswith("missing-"):
            body = {"statusCode": 404, "body": json.dumps({"error": "not_found"})}
        else:
            body = {"statusCode": 200, "body": json.dumps({"order_id": item})}
        return {"ResponseMetadata": {"RequestId": f"r{self.n}"}, "Payload": io.BytesIO(json.dumps(body).encode())}


def test_a_crash_mid_episode_restores_the_deployed_settings_and_keeps_every_call_made(tmp_path, monkeypatch):
    monkeypatch.setattr("sflad.aws.workload.time.sleep", lambda s: None)
    lam = Config()
    with pytest.raises(ConnectionError):
        # 2 training cycles make 4 calls; the 6th call is the second call of the fault burst
        run_evaluation("orders", APP, CFG, 1, tmp_path, lam=lam, invoker=Invoker(fail_at=6), account=ACCOUNT)
    assert lam.updates[-1] == BASELINE
    saved = [json.loads(line) for line in (tmp_path / "invocations.jsonl").read_text().splitlines()]
    assert [r["phase"] for r in saved] == ["train"] * 4 + ["fault"]
    meta = json.loads((tmp_path / "run.json").read_text())
    assert set(meta["times"]) == {"start", "train_end"}


def test_a_full_small_run_records_every_phase(tmp_path, monkeypatch):
    monkeypatch.setattr("sflad.aws.workload.time.sleep", lambda s: None)
    monkeypatch.setattr("sflad.aws.evaluation_run.time.sleep", lambda s: None)
    out = run_evaluation("orders", APP, CFG, 1, tmp_path, lam=Config(), invoker=Invoker(fail_at=-1), account=ACCOUNT)
    assert [r["phase"] for r in out["records"]].count("control") == 2 + 2
    assert set(out["times"]) == {"start", "train_end", "control_start", "end"}
    assert [json.loads(line)["episode"] for line in (tmp_path / "episodes.jsonl").read_text().splitlines()] == ["config-00"]
    assert not any(r["content_ok"] is False for r in out["records"])
    meta = json.loads((tmp_path / "run.json").read_text())
    train = [r["end_ms"] - r["start_ms"] for r in out["records"] if r["phase"] == "train"]
    assert meta["slow_limit_ms"] == out["slow_limit_ms"] == max(train) + 1000


def test_episodes_of_every_category_run_in_one_shuffled_order_and_the_delays_alternate(tmp_path, monkeypatch):
    monkeypatch.setattr("sflad.aws.workload.time.sleep", lambda s: None)
    monkeypatch.setattr("sflad.aws.evaluation_run.time.sleep", lambda s: None)
    cfg = {**CFG, "faults": {**CFG["faults"], "categories": ["config", "latency"], "injections_per_category": 4}}
    lam = Config()
    run_evaluation("orders", APP, cfg, 3, tmp_path, lam=lam, invoker=Invoker(fail_at=-1), account=ACCOUNT)
    episodes = [json.loads(line) for line in (tmp_path / "episodes.jsonl").read_text().splitlines()]
    names = [e["episode"] for e in episodes]
    assert sorted(names) == [f"{c}-{i:02d}" for c in ("config", "latency") for i in range(4)]
    assert names != sorted(names)  # interleaved
    assert {e["episode"]: e.get("strength_ms") for e in episodes if e["category"] == "latency"} == {
        "latency-00": 4000, "latency-01": 6000, "latency-02": 4000, "latency-03": 6000}
    delays = [u["Environment"]["Variables"]["INJECTED_DELAY_MS"] for u in lam.updates
              if "Environment" in u and u["Environment"]["Variables"]["INJECTED_DELAY_MS"] != "0"]
    assert sorted(delays) == ["4000", "4000", "6000", "6000"]


def test_deployment_record_names_the_creation_times(monkeypatch):
    from sflad.aws import evaluation_run

    class Logs:
        def describe_log_groups(self, logGroupNamePrefix):
            return {"logGroups": [{"logGroupName": logGroupNamePrefix, "creationTime": 1700000000000},
                                  {"logGroupName": logGroupNamePrefix + "-other", "creationTime": 1}]}

    class Lam:
        def get_function_configuration(self, FunctionName):
            return {"LastModified": "2026-11-01T10:00:00.000+0000"}

    monkeypatch.setattr(evaluation_run, "make_client", lambda service, region=None: Logs() if service == "logs" else Lam())
    record = evaluation_run.deployment_record({"log_group": "/aws/lambda/x", "function_name": "x"}, "eu-west-1")
    assert record["log_group_created_ms"] == 1700000000000
    assert record["function_last_modified"].startswith("2026-11-01")


def test_the_run_record_never_holds_the_account_id(tmp_path, monkeypatch):
    monkeypatch.setattr("sflad.aws.workload.time.sleep", lambda s: None)
    monkeypatch.setattr("sflad.aws.evaluation_run.time.sleep", lambda s: None)
    run_evaluation("orders", APP, CFG, 1, tmp_path, lam=Config(), invoker=Invoker(fail_at=-1), account=ACCOUNT)
    text = (tmp_path / "run.json").read_text()
    assert ACCOUNT not in text and json.loads(text)["deployed"]["role_arn"] == "arn:aws:iam::<ACCOUNT>:role/r"


def test_the_exported_logs_never_hold_the_account_id(tmp_path, monkeypatch):
    from sflad.aws import evaluation_run
    line = f"AccessDeniedException: User: arn:aws:sts::{ACCOUNT}:assumed-role/r is not authorized"
    monkeypatch.setattr(evaluation_run.time, "sleep", lambda s: None)
    monkeypatch.setattr(evaluation_run, "export_events", lambda *a, **k: [{"message": line, "timestamp": 1}])
    seen = []
    monkeypatch.setattr(evaluation_run, "label_events", lambda raw, *a: seen.extend(raw) or [])
    cfg = {"export": {"attempts": 1, "wait_seconds": 0}, "region": "eu-west-1"}
    evaluation_run.export_run({"log_group": "g"}, cfg, tmp_path, [], [], {"start": 0}, ACCOUNT, 3000)
    assert ACCOUNT not in (tmp_path / "cloudwatch_events.jsonl").read_text()
    assert seen[0]["message"] == line.replace(ACCOUNT, "<ACCOUNT>")
