from sqlalchemy.orm import Session

from backend_app.crud.base import CRUDBase
from backend_app.models.item import Item


class CRUDItem(CRUDBase):
    def get_multi_by_owner(self, db: Session, owner_id: int) -> list[Item]:
        return (
            db.query(self.model)
            .filter(self.model.owner_id == owner_id)
            .all()
        )

    def get_by_owner(self, db: Session, id: int, owner_id: int) -> Item | None:
        return (
            db.query(self.model)
            .filter(self.model.id == id, self.model.owner_id == owner_id)
            .first()
        )


item_crud = CRUDItem(Item)
