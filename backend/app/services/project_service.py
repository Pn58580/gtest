from app.schemas.project import Project


class ProjectService:
    """Temporary in-memory service; swap to ORM repository later."""

    def list_projects(self) -> list[Project]:
        return [
            Project(id=1, name="Demo API Project", owner="admin"),
            Project(id=2, name="Demo Web Project", owner="qa_lead"),
        ]


project_service = ProjectService()
