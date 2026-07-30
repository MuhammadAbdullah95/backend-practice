from sqlalchemy.orm import Session

from backend_app.crud.base import CRUDBase
from backend_app.models.user import User


class CRUDUser(CRUDBase):
    def get_by_username(self, db: Session, username: str) -> User | None:
        return (
            db.query(self.model)
            .filter(self.model.username == username)
            .first()
        )

    def get_all(self, db: Session) -> list[User]:
        return db.query(self.model).all()


user_crud = CRUDUser(User)
