from sqlalchemy.orm import Session

from backend_app.crud.base import CRUDBase
from backend_app.models.user import User


class CRUDUser(CRUDBase):
    def get_by_username(self, db: Session, username: str) -> User | None:
        return db.query(self.model).filter(self.model.username == username).first()


user_crud = CRUDUser(User)
