from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Environment(Base):
    __tablename__ = 'proj_env'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('proj_project.id'))
    name: Mapped[str] = mapped_column(String(64))
    base_url: Mapped[str] = mapped_column(String(255))
    variables_json: Mapped[str] = mapped_column(Text, default='{}')
