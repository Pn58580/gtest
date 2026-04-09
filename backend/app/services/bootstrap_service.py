from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import engine
from app.models import Base
from app.models.project import Project
from app.models.user import User
from app.services.api_case_service import api_case_service
from app.services.project_service import project_service
from app.services.user_service import user_service


def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)
    user_service.create_admin_if_not_exists(db)
    admin = db.scalar(select(User).where(User.username == "admin"))
    if admin:
        project_service.seed_demo_projects(db, owner_id=admin.id)

    first_project = db.scalar(select(Project).order_by(Project.id.asc()))
    if first_project:
        api_case_service.seed_demo_case(db, project_id=first_project.id)
