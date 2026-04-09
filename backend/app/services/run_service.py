from app.runners.api_runner import ApiRunner
from app.runners.app_runner import AppRunner
from app.runners.base import BaseRunner
from app.runners.web_runner import WebRunner
from app.schemas.common import RunRequest, RunResult


class RunService:
    def __init__(self) -> None:
        self._runners: dict[str, BaseRunner] = {
            "api": ApiRunner(),
            "web": WebRunner(),
            "app": AppRunner(),
        }

    def execute(self, request: RunRequest) -> RunResult:
        runner = self._runners[request.engine]
        return runner.run(request)


run_service = RunService()
