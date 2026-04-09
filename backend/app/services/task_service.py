from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.scheduler import scheduler
from app.models.task import TaskSchedule
from app.schemas.common import RunRequest
from app.schemas.task import ScheduleRequest
from app.services.run_service import run_service


class TaskService:
    def create_schedule(self, db: Session, payload: ScheduleRequest, creator: str) -> TaskSchedule:
        row = TaskSchedule(
            name=payload.name,
            cron=payload.cron,
            engine=payload.engine,
            project_id=payload.project_id,
            case_id=payload.case_id,
            created_by=creator,
        )
        db.add(row)
        db.commit()
        db.refresh(row)

        trigger = CronTrigger.from_crontab(payload.cron)
        scheduler.add_job(
            self._run_job,
            trigger=trigger,
            id=f"task-{row.id}",
            replace_existing=True,
            kwargs={
                "project_id": row.project_id,
                "case_id": row.case_id,
                "engine": row.engine,
                "triggered_by": f"scheduler:{row.created_by}",
            },
        )
        return row

    def list_schedules(self, db: Session) -> list[TaskSchedule]:
        return db.scalars(select(TaskSchedule).order_by(TaskSchedule.id.desc())).all()

    @staticmethod
    def _run_job(project_id: int, case_id: int, engine: str, triggered_by: str) -> None:
        from app.db.session import SessionLocal

        db = SessionLocal()
        try:
            request = RunRequest(
                project_id=project_id,
                case_id=case_id,
                engine=engine,
                triggered_by=triggered_by,
            )
            run_service.execute(db, request)
        finally:
            db.close()


task_service = TaskService()
