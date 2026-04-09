from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User


class UserService:
    def create_admin_if_not_exists(self, db: Session) -> None:
        existing = db.scalar(select(User).where(User.username == "admin"))
        if existing:
            return
        db.add(User(username="admin", password_hash=hash_password("admin123"), role="admin"))
        db.commit()

    def get_by_username(self, db: Session, username: str) -> User | None:
        return db.scalar(select(User).where(User.username == username))

    def authenticate(self, db: Session, username: str, password: str) -> User | None:
        user = self.get_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user


user_service = UserService()
