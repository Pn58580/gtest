from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.environment import Environment
from app.schemas.environment import EnvCreate, EnvItem


class EnvironmentService:
    def list_envs(self, db: Session, project_id: int | None = None) -> list[EnvItem]:
        stmt = select(Environment).order_by(Environment.id.desc())
        if project_id:
            stmt = stmt.where(Environment.project_id == project_id)
        rows = db.scalars(stmt).all()
        return [EnvItem.model_validate(row) for row in rows]

    def create_env(self, db: Session, payload: EnvCreate) -> EnvItem:
        row = Environment(**payload.model_dump())
        db.add(row)
        db.commit()
        db.refresh(row)
        return EnvItem.model_validate(row)

    def delete_env(self, db: Session, env_id: int) -> bool:
        row = db.get(Environment, env_id)
        if not row:
            return False
        db.delete(row)
        db.commit()
        return True

    def seed_default_env(self, db: Session, project_id: int) -> None:
        exists = db.scalar(select(Environment).where(Environment.project_id == project_id).limit(1))
        if exists:
            return
        db.add(
            Environment(
                project_id=project_id,
                name='dev',
                base_url='http://127.0.0.1:8000',
                variables_json='{"token":"demo"}',
            )
        )
        db.commit()


environment_service = EnvironmentService()
