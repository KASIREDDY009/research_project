"""Infrastructure faults for one application, injected and restored one episode at a time.

Categories: permission (a role that may only write logs), config (a table that does not exist),
timeout (DynamoDB unreachable), resource (memory below the working set) and latency (the application
waits a set time before handling each request, so calls succeed but slowly).
A sham configuration update starts new execution environments without a fault.
"""

from __future__ import annotations

from typing import Any, Dict


class Faults:
    def __init__(self, lam, app: Dict[str, Any], cfg: Dict[str, Any]) -> None:
        self.lam, self.app = lam, app
        self.fault_timeout = int(cfg["fault_timeout_seconds"])
        self.endpoint = str(cfg["unreachable_endpoint"])
        self.starved_memory = int(cfg["starved_memory_mb"])
        self.delays_ms = [int(d) for d in cfg["injected_delays_ms"]]
        self.deployed = {
            "Environment": {"Variables": dict(app["environment"])},
            "Timeout": int(app["timeout_seconds"]),
            "MemorySize": int(app["memory_size"]),
            "Role": app["role_arn"],
        }
        self.revision = 0

    def _update(self, **settings: Any) -> None:
        name = self.app["function_name"]
        waiter = self.lam.get_waiter("function_updated_v2")
        waiter.wait(FunctionName=name)
        self.lam.update_function_configuration(FunctionName=name, **settings)
        waiter.wait(FunctionName=name)

    def _env(self, **extra: str) -> Dict[str, Any]:
        return {"Variables": {**self.deployed["Environment"]["Variables"], **extra}}

    def strength(self, category: str, index: int) -> int | None:
        return self.delays_ms[index % len(self.delays_ms)] if category == "latency" else None

    def inject(self, category: str, index: int) -> None:
        if category == "permission":
            self._update(Role=self.app["logs_role_arn"])
        elif category == "config":
            self._update(Environment=self._env(TABLE_NAME=self.app["table_name"] + "-missing"))
        elif category == "timeout":
            self._update(Environment=self._env(AWS_ENDPOINT_URL_DYNAMODB=self.endpoint), Timeout=self.fault_timeout)
        elif category == "resource":
            self._update(MemorySize=self.starved_memory)
        elif category == "latency":
            self._update(Environment=self._env(INJECTED_DELAY_MS=str(self.strength(category, index))))
        else:
            raise ValueError(f"unknown fault category {category!r}")

    def sham(self) -> None:
        """A configuration change that alters nothing the function does."""
        self.revision += 1
        self._update(Environment=self._env(CONFIG_REVISION=str(self.revision)))

    def restore_all(self) -> None:
        """Put back the deployed settings, whatever state an interrupted run left behind."""
        self._update(**self.deployed)
