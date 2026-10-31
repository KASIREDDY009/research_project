from __future__ import annotations

import pytest

from sflad.aws.faults import Faults

APP = {"function_name": "fn", "role_arn": "arn:role", "logs_role_arn": "arn:logs-role", "table_name": "tbl",
       "timeout_seconds": 10, "memory_size": 512,
       "environment": {"TABLE_NAME": "tbl", "LOG_LEVEL": "INFO", "REFERENCE_DATA_SIZE": "10", "INJECTED_DELAY_MS": "0"}}
CFG = {"fault_timeout_seconds": 3, "unreachable_endpoint": "https://10.255.255.1", "starved_memory_mb": 128,
       "injected_delays_ms": [4000, 6000]}
BASELINE = {"Environment": {"Variables": APP["environment"]}, "Timeout": 10, "MemorySize": 512, "Role": "arn:role"}


class _Waiter:
    def wait(self, **kw):
        pass


class FakeLambda:
    def __init__(self):
        self.updates = []

    def get_waiter(self, name):
        assert name == "function_updated_v2"
        return _Waiter()

    def update_function_configuration(self, FunctionName, **settings):
        self.updates.append(settings)


@pytest.fixture
def made():
    lam = FakeLambda()
    return Faults(lam, APP, CFG), lam


def test_each_category_changes_only_what_it_names(made):
    f, lam = made
    f.inject("config", 0)
    assert lam.updates[-1] == {"Environment": {"Variables": {**APP["environment"], "TABLE_NAME": "tbl-missing"}}}
    f.inject("timeout", 0)
    assert lam.updates[-1] == {"Environment": {"Variables": {**APP["environment"],
                               "AWS_ENDPOINT_URL_DYNAMODB": "https://10.255.255.1"}}, "Timeout": 3}
    f.inject("resource", 0)
    assert lam.updates[-1] == {"MemorySize": 128}
    f.inject("permission", 0)
    assert lam.updates[-1] == {"Role": "arn:logs-role"}
    f.inject("latency", 0)
    assert lam.updates[-1] == {"Environment": {"Variables": {**APP["environment"], "INJECTED_DELAY_MS": "4000"}}}
    f.inject("latency", 1)
    assert lam.updates[-1] == {"Environment": {"Variables": {**APP["environment"], "INJECTED_DELAY_MS": "6000"}}}
    assert (f.strength("latency", 2), f.strength("config", 0)) == (4000, None)


def test_restore_returns_to_the_deployed_settings(made):
    f, lam = made
    for category in ("permission", "config", "timeout", "resource", "latency"):
        f.inject(category, 0)
        f.restore_all()
        assert lam.updates[-1] == BASELINE
    f.restore_all()
    assert lam.updates[-1] == BASELINE


def test_sham_updates_change_nothing_the_function_does(made):
    f, lam = made
    f.sham()
    f.sham()
    assert [u["Environment"]["Variables"]["CONFIG_REVISION"] for u in lam.updates] == ["1", "2"]
    assert all({k: v for k, v in u["Environment"]["Variables"].items() if k != "CONFIG_REVISION"}
               == APP["environment"] for u in lam.updates)


def test_an_unknown_category_is_refused(made):
    with pytest.raises(ValueError):
        made[0].inject("network", 0)
