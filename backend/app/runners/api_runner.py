from uuid import uuid4

from app.runners.base import BaseRunner
from app.schemas.common import RunRequest, RunResult, StepResult


class ApiRunner(BaseRunner):
    engine_name = "api"

    def run(self, request: RunRequest) -> RunResult:
        path = str(request.params.get('path', '/'))
        expected_status = int(request.params.get('expected_status', 200))
        expected_keyword = str(request.params.get('expected_keyword', '')).strip()

        # 模拟响应
        if path == '/health':
            response_status = 200
            response_text = '{"status":"ok"}'
        else:
            response_status = 404
            response_text = '{"detail":"not found"}'

        status_ok = response_status == expected_status
        keyword_ok = True if not expected_keyword else expected_keyword in response_text
        final_ok = status_ok and keyword_ok

        return RunResult(
            run_id=str(uuid4()),
            engine="api",
            status="passed" if final_ok else "failed",
            duration_ms=320,
            steps=[
                StepResult(name="build_request", status="passed", message="request built"),
                StepResult(name="send_request", status="passed", message=f"{response_status}"),
                StepResult(
                    name="assert_status",
                    status="passed" if status_ok else "failed",
                    message=f"expected={expected_status}, actual={response_status}",
                ),
                StepResult(
                    name="assert_keyword",
                    status="passed" if keyword_ok else "failed",
                    message=f"expected keyword={expected_keyword or '<none>'}",
                ),
            ],
        )
