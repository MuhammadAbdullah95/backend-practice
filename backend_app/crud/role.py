from sqlalchemy.orm import Session

from backend_app.crud.base import CRUDBase
from backend_app.models.role import Role


class CRUDRole(CRUDBase):
    def get_by_name(self, db: Session, name: str) -> Role | None:
        return db.query(self.model).filter(self.model.name == name).first()

    def get_all(self, db: Session) -> list[Role]:
        return db.query(self.model).all()


role_crud = CRUDRole(Role)
