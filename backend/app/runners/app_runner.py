from uuid import uuid4

from app.runners.base import BaseRunner
from app.schemas.common import RunRequest, RunResult, StepResult


class AppRunner(BaseRunner):
    engine_name = "app"

    def run(self, request: RunRequest) -> RunResult:
        return RunResult(
            run_id=str(uuid4()),
            engine="app",
            status="passed",
            duration_ms=1340,
            steps=[
                StepResult(name="connect_device", status="passed", message="device online"),
                StepResult(name="execute_airtest", status="passed", message="script done"),
            ],
        )
