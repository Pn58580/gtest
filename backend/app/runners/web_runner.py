from uuid import uuid4

from app.runners.base import BaseRunner
from app.schemas.common import RunRequest, RunResult, StepResult


class WebRunner(BaseRunner):
    engine_name = "web"

    def run(self, request: RunRequest) -> RunResult:
        page_url = str(request.params.get('page_url', 'https://example.com'))
        selector = str(request.params.get('selector', 'h1'))
        expect_text = str(request.params.get('expect_text', 'Example')).strip()
        env_name = str(request.params.get('env_name', '')).strip()

        simulated_text = 'Example Domain' if 'example.com' in page_url else 'Unknown Page'
        assert_ok = expect_text in simulated_text if expect_text else True

        return RunResult(
            run_id=str(uuid4()),
            engine="web",
            status="passed" if assert_ok else "failed",
            duration_ms=890,
            steps=[
                StepResult(name="launch_browser", status="passed", message=f"env={env_name or 'default'}"),
                StepResult(name="open_page", status="passed", message=page_url),
                StepResult(
                    name='assert_dom_text',
                    status='passed' if assert_ok else 'failed',
                    message=f"selector={selector}, expect={expect_text}",
                ),
            ],
        )
