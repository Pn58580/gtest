from uuid import uuid4

from app.runners.base import BaseRunner
from app.schemas.common import RunRequest, RunResult, StepResult


class WebRunner(BaseRunner):
    engine_name = "web"

    def run(self, request: RunRequest) -> RunResult:
        return RunResult(
            run_id=str(uuid4()),
            engine="web",
            status="passed",
            duration_ms=890,
            steps=[
                StepResult(name="launch_browser", status="passed", message="chromium started"),
                StepResult(name="execute_actions", status="passed", message="actions done"),
            ],
        )
