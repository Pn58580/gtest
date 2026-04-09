import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import TaskRun
from app.schemas.report import ReportResponse


class ReportService:
    def get_by_run_id(self, db: Session, run_id: str) -> ReportResponse | None:
        row = db.scalar(select(TaskRun).where(TaskRun.run_id == run_id))
        if not row:
            return None
        detail = json.loads(row.detail_json)
        return ReportResponse(
            run_id=row.run_id,
            engine=row.engine,
            status=row.status,
            duration_ms=row.duration_ms,
            triggered_by=row.triggered_by,
            steps=detail.get("steps", []),
        )


report_service = ReportService()
