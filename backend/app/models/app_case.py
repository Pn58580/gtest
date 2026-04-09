from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AppCase(Base):
    __tablename__ = 'app_case'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('proj_project.id'))
    name: Mapped[str] = mapped_column(String(128))
    device_id: Mapped[str] = mapped_column(String(64), default='emulator-5554')
    script_path: Mapped[str] = mapped_column(String(255), default='scripts/demo.air')
    assert_keyword: Mapped[str] = mapped_column(String(128), default='success')
