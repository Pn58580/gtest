import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.app_case import AppCase
from app.schemas.app_case import AppCaseCreate, AppCaseItem, AppStep


class AppCaseService:
    def list_cases(self, db: Session, project_id: int | None = None) -> list[AppCaseItem]:
        stmt = select(AppCase).order_by(AppCase.id.desc())
        if project_id:
            stmt = stmt.where(AppCase.project_id == project_id)
        rows = db.scalars(stmt).all()
        return [self._to_item(row) for row in rows]

    def create_case(self, db: Session, payload: AppCaseCreate) -> AppCaseItem:
        row = AppCase(
            project_id=payload.project_id,
            name=payload.name,
            device_id=payload.device_id,
            app_package=payload.app_package,
            app_activity=payload.app_activity,
            script_path=payload.script_path,
            steps_json=json.dumps([item.model_dump() for item in payload.steps], ensure_ascii=False),
            assert_keyword=payload.assert_keyword,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return self._to_item(row)

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

    @staticmethod
    def _to_item(row: AppCase) -> AppCaseItem:
        try:
            raw_steps = json.loads(row.steps_json or '[]')
        except json.JSONDecodeError:
            raw_steps = []
        if not isinstance(raw_steps, list):
            raw_steps = []
        steps = [AppStep.model_validate(item) for item in raw_steps if isinstance(item, dict)]
        return AppCaseItem(
            id=row.id,
            project_id=row.project_id,
            name=row.name,
            device_id=row.device_id,
            app_package=row.app_package,
            app_activity=row.app_activity,
            script_path=row.script_path,
            steps=steps,
            assert_keyword=row.assert_keyword,
        )


app_case_service = AppCaseService()
