from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class TaskSchedule(Base):
    __tablename__ = "task_schedule"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    cron: Mapped[str] = mapped_column(String(64))
    engine: Mapped[str] = mapped_column(String(16))
    project_id: Mapped[int] = mapped_column(ForeignKey("proj_project.id"))
    case_id: Mapped[int] = mapped_column()
    created_by: Mapped[str] = mapped_column(String(64))


class TaskRun(Base):
    __tablename__ = "task_run"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    engine: Mapped[str] = mapped_column(String(16))
    status: Mapped[str] = mapped_column(String(16))
    duration_ms: Mapped[int] = mapped_column()
    triggered_by: Mapped[str] = mapped_column(String(64))
    detail_json: Mapped[str] = mapped_column(Text)
