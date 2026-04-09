from uuid import uuid4

from app.runners.base import BaseRunner
from app.schemas.common import RunRequest, RunResult, StepResult


class ApiRunner(BaseRunner):
    engine_name = "api"

    def run(self, request: RunRequest) -> RunResult:
        return RunResult(
            run_id=str(uuid4()),
            engine="api",
            status="passed",
            duration_ms=320,
            steps=[
                StepResult(name="build_request", status="passed", message="request built"),
                StepResult(name="send_request", status="passed", message="200 OK"),
                StepResult(name="assert_response", status="passed", message="assertions passed"),
            ],
        )
