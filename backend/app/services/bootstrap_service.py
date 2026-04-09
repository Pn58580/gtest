from sqlalchemy import inspect, select, text
from sqlalchemy.orm import Session

from app.db.session import engine
from app.models import Base
from app.models.project import Project
from app.models.user import User
from app.services.api_case_service import api_case_service
from app.services.environment_service import environment_service
from app.services.project_service import project_service
from app.services.user_service import user_service


def _migrate_legacy_schema(db: Session) -> None:
    """Lightweight migration for older local DB files without Alembic."""
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())

    if 'api_case' in tables:
        cols = {col['name'] for col in inspector.get_columns('api_case')}
        if 'expected_status' not in cols:
            db.execute(text('ALTER TABLE api_case ADD COLUMN expected_status INTEGER DEFAULT 200'))
        if 'expected_keyword' not in cols:
            db.execute(text("ALTER TABLE api_case ADD COLUMN expected_keyword VARCHAR(128) DEFAULT ''"))

    if 'proj_env' in tables:
        cols = {col['name'] for col in inspector.get_columns('proj_env')}
        if 'variables_json' not in cols:
            db.execute(text("ALTER TABLE proj_env ADD COLUMN variables_json TEXT DEFAULT '{}'"))

    db.commit()


def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)
    _migrate_legacy_schema(db)

    user_service.create_admin_if_not_exists(db)
    admin = db.scalar(select(User).where(User.username == "admin"))
    if admin:
        project_service.seed_demo_projects(db, owner_id=admin.id)

    first_project = db.scalar(select(Project).order_by(Project.id.asc()))
    if first_project:
        environment_service.seed_default_env(db, project_id=first_project.id)
        api_case_service.seed_demo_case(db, project_id=first_project.id)
