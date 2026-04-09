from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.api_case import ApiCase
from app.schemas.api_case import ApiCaseCreate, ApiCaseItem


class ApiCaseService:
    def list_cases(self, db: Session, project_id: int | None = None) -> list[ApiCaseItem]:
        stmt = select(ApiCase).order_by(ApiCase.id.desc())
        if project_id:
            stmt = stmt.where(ApiCase.project_id == project_id)
        rows = db.scalars(stmt).all()
        return [ApiCaseItem.model_validate(row) for row in rows]

    def create_case(self, db: Session, payload: ApiCaseCreate) -> ApiCaseItem:
        row = ApiCase(**payload.model_dump())
        db.add(row)
        db.commit()
        db.refresh(row)
        return ApiCaseItem.model_validate(row)

    def get_case(self, db: Session, case_id: int) -> ApiCase | None:
        return db.get(ApiCase, case_id)

    def delete_case(self, db: Session, case_id: int) -> bool:
        row = self.get_case(db, case_id)
        if not row:
            return False
        db.delete(row)
        db.commit()
        return True

    def seed_demo_case(self, db: Session, project_id: int) -> None:
        exists = db.scalar(select(ApiCase).where(ApiCase.project_id == project_id).limit(1))
        if exists:
            return
        db.add(
            ApiCase(
                project_id=project_id,
                name='健康检查接口',
                method='GET',
                path='/health',
                body='{}',
                expected_status=200,
                expected_keyword='ok',
            )
        )
        db.commit()


api_case_service = ApiCaseService()
