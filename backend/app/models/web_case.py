from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class WebCase(Base):
    __tablename__ = 'web_case'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('proj_project.id'))
    name: Mapped[str] = mapped_column(String(128))
    page_url: Mapped[str] = mapped_column(String(255), default='https://example.com')
    selector: Mapped[str] = mapped_column(String(128), default='h1')
    expect_text: Mapped[str] = mapped_column(String(128), default='Example')
