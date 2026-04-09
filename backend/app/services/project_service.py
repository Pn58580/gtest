from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project as ProjectModel
from app.schemas.project import Project


class ProjectService:
    def list_projects(self, db: Session) -> list[Project]:
        rows = db.scalars(select(ProjectModel)).all()
        return [Project.model_validate(row) for row in rows]

    def seed_demo_projects(self, db: Session, owner_id: int) -> None:
        if db.scalar(select(ProjectModel).limit(1)):
            return
        db.add_all(
            [
                ProjectModel(name="Demo API Project", owner_id=owner_id),
                ProjectModel(name="Demo Web Project", owner_id=owner_id),
            ]
        )
        db.commit()


project_service = ProjectService()
