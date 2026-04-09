from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.app_case import AppCase
from app.schemas.app_case import AppCaseCreate, AppCaseItem


class AppCaseService:
    def list_cases(self, db: Session, project_id: int | None = None) -> list[AppCaseItem]:
        stmt = select(AppCase).order_by(AppCase.id.desc())
        if project_id:
            stmt = stmt.where(AppCase.project_id == project_id)
        rows = db.scalars(stmt).all()
        return [AppCaseItem.model_validate(row) for row in rows]

    def create_case(self, db: Session, payload: AppCaseCreate) -> AppCaseItem:
        row = AppCase(**payload.model_dump())
        db.add(row)
        db.commit()
        db.refresh(row)
        return AppCaseItem.model_validate(row)

    def get_case(self, db: Session, case_id: int) -> AppCase | None:
        return db.get(AppCase, case_id)

    def delete_case(self, db: Session, case_id: int) -> bool:
        row = self.get_case(db, case_id)
        if not row:
            return False
        db.delete(row)
        db.commit()
        return True

    def seed_demo_case(self, db: Session, project_id: int) -> None:
        exists = db.scalar(select(AppCase).where(AppCase.project_id == project_id).limit(1))
        if exists:
            return
        db.add(
            AppCase(
                project_id=project_id,
                name='App 登录冒烟',
                device_id='emulator-5554',
                app_package='com.demo.app',
                app_activity='com.demo.app.MainActivity',
                script_path='scripts/login_smoke.air',
                steps_json='[{"action":"launch_app"},{"action":"input","target":"id=username","value":"demo"},{"action":"tap","target":"id=login"},{"action":"assert_text","target":"id=welcome","value":"Welcome"}]',
                assert_keyword='Welcome',
            )
        )
        db.commit()


app_case_service = AppCaseService()
