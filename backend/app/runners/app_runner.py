from uuid import uuid4

from app.runners.base import BaseRunner
from app.schemas.common import RunRequest, RunResult, StepResult


class AppRunner(BaseRunner):
    engine_name = "app"

    def run(self, request: RunRequest) -> RunResult:
        device_id = str(request.params.get('device_id', 'emulator-5554'))
        script_path = str(request.params.get('script_path', 'scripts/demo.air'))
        expect = str(request.params.get('assert_keyword', 'success')).strip()

        # 模拟 Airtest 执行日志
        output = f"device={device_id}; script={script_path}; result=success"
        keyword_ok = expect in output if expect else True

        return RunResult(
            run_id=str(uuid4()),
            engine="app",
            status="passed" if keyword_ok else "failed",
            duration_ms=1340,
            steps=[
                StepResult(name="connect_device", status="passed", message=f"{device_id} online"),
                StepResult(name="execute_airtest", status="passed", message=script_path),
                StepResult(
                    name='assert_output',
                    status='passed' if keyword_ok else 'failed',
                    message=f"expect keyword={expect or '<none>'}",
                ),
            ],
        )
