from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend_app.api.deps import get_current_user
from backend_app.crud.item import item_crud
from backend_app.database import get_db
from backend_app.models.user import User
from backend_app.schemas.item import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.post("", status_code=201, response_model=ItemResponse)
def create_item(
    item: ItemCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return item_crud.create(db, **item.model_dump(), owner_id=current_user.id)


@router.get("", response_model=list[ItemResponse])
def list_items(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return item_crud.get_multi_by_owner(db, owner_id=current_user.id)


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    item = item_crud.get_by_owner(db, id=item_id, owner_id=current_user.id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item: ItemUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    db_item = item_crud.get_by_owner(db, id=item_id, owner_id=current_user.id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_crud.update(db, db_obj=db_item, update_data=item.model_dump())


@router.delete("/{item_id}", status_code=204)
def delete_item(
    item_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    db_item = item_crud.get_by_owner(db, id=item_id, owner_id=current_user.id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_crud.remove(db, db_obj=db_item)
