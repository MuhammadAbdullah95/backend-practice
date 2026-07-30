from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend_app.api.deps import RoleChecker, get_current_user
from backend_app.crud.item import item_crud
from backend_app.crud.role import role_crud
from backend_app.crud.user import user_crud
from backend_app.database import get_db
from backend_app.models.user import User
from backend_app.schemas.item import ItemResponse
from backend_app.schemas.role import RoleResponse
from backend_app.schemas.user import UserResponse, UserRoleUpdate

router = APIRouter(prefix="/admin", tags=["admin"])

admin_only = RoleChecker(["admin"])
admin_or_manager = RoleChecker(["admin", "manager"])


@router.get("/users", response_model=list[UserResponse])
def list_users(
    _: Annotated[User, Depends(admin_only)],
    db: Session = Depends(get_db),
):
    return user_crud.get_all(db)


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    _: Annotated[User, Depends(admin_only)],
    db: Session = Depends(get_db),
):
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/users/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    body: UserRoleUpdate,
    _: Annotated[User, Depends(admin_only)],
    db: Session = Depends(get_db),
):
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    role = role_crud.get(db, id=body.role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return user_crud.update(db, db_obj=user, update_data={"role_id": body.role_id})


@router.get("/roles", response_model=list[RoleResponse])
def list_roles(
    _: Annotated[User, Depends(admin_only)],
    db: Session = Depends(get_db),
):
    return role_crud.get_all(db)


@router.get("/items", response_model=list[ItemResponse])
def list_all_items(
    _: Annotated[User, Depends(admin_or_manager)],
    db: Session = Depends(get_db),
):
    return item_crud.get_multi(db)


@router.get("/items/{item_id}", response_model=ItemResponse)
def get_any_item(
    item_id: int,
    _: Annotated[User, Depends(admin_or_manager)],
    db: Session = Depends(get_db),
):
    item = item_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/items/{item_id}", status_code=204)
def delete_any_item(
    item_id: int,
    _: Annotated[User, Depends(admin_or_manager)],
    db: Session = Depends(get_db),
):
    item = item_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_crud.remove(db, db_obj=item)
