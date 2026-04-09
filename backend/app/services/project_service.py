from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project as ProjectModel
from app.schemas.project import Project


class ProjectService:
    def list_projects(self, db: Session) -> list[Project]:
        rows = db.scalars(select(ProjectModel).order_by(ProjectModel.id.desc())).all()
        return [Project.model_validate(row) for row in rows]

    def create_project(self, db: Session, name: str, owner_id: int) -> Project:
        row = ProjectModel(name=name, owner_id=owner_id)
        db.add(row)
        db.commit()
        db.refresh(row)
        return Project.model_validate(row)

    def delete_project(self, db: Session, project_id: int) -> bool:
        row = db.get(ProjectModel, project_id)
        if not row:
            return False
        db.delete(row)
        db.commit()
        return True

    def seed_demo_projects(self, db: Session, owner_id: int) -> None:
        if db.scalar(select(ProjectModel).limit(1)):
            return
        db.add_all(
            [
                ProjectModel(name="Demo API Project", owner_id=owner_id),
                ProjectModel(name="Demo Web Project", owner_id=owner_id),
                ProjectModel(name="Demo App Project", owner_id=owner_id),
            ]
        )
        db.commit()


project_service = ProjectService()
