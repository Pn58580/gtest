from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ApiCase(Base):
    __tablename__ = 'api_case'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('proj_project.id'))
    name: Mapped[str] = mapped_column(String(128))
    method: Mapped[str] = mapped_column(String(10), default='GET')
    path: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text, default='{}')
