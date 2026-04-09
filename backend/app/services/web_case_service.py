from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.web_case import WebCase
from app.schemas.web_case import WebCaseCreate, WebCaseItem


class WebCaseService:
    def list_cases(self, db: Session, project_id: int | None = None) -> list[WebCaseItem]:
        stmt = select(WebCase).order_by(WebCase.id.desc())
        if project_id:
            stmt = stmt.where(WebCase.project_id == project_id)
        rows = db.scalars(stmt).all()
        return [WebCaseItem.model_validate(row) for row in rows]

    def create_case(self, db: Session, payload: WebCaseCreate) -> WebCaseItem:
        row = WebCase(**payload.model_dump())
        db.add(row)
        db.commit()
        db.refresh(row)
        return WebCaseItem.model_validate(row)

    def get_case(self, db: Session, case_id: int) -> WebCase | None:
        return db.get(WebCase, case_id)

    def delete_case(self, db: Session, case_id: int) -> bool:
        row = self.get_case(db, case_id)
        if not row:
            return False
        db.delete(row)
        db.commit()
        return True

    def seed_demo_case(self, db: Session, project_id: int) -> None:
        exists = db.scalar(select(WebCase).where(WebCase.project_id == project_id).limit(1))
        if exists:
            return
        db.add(
            WebCase(
                project_id=project_id,
                name='Web 首页标题检查',
                page_url='https://example.com',
                selector='h1',
                expect_text='Example',
            )
        )
        db.commit()


web_case_service = WebCaseService()
