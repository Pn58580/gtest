import json

from sqlalchemy.orm import Session

from app.models.task import TaskRun
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

    def execute(self, db: Session, request: RunRequest) -> RunResult:
        runner = self._runners[request.engine]
        result = runner.run(request)
        db.add(
            TaskRun(
                run_id=result.run_id,
                engine=result.engine,
                status=result.status,
                duration_ms=result.duration_ms,
                triggered_by=request.triggered_by,
                detail_json=json.dumps(result.model_dump(mode="json"), ensure_ascii=False),
            )
        )
        db.commit()
        return result


run_service = RunService()
