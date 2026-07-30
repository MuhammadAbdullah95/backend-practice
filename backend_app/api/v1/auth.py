from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend_app.api.deps import get_current_user
from backend_app.core.security import create_access_token, hash_password, verify_password
from backend_app.crud.user import user_crud
from backend_app.database import get_db
from backend_app.models.user import User
from backend_app.schemas.token import Token
from backend_app.schemas.user import UserCreate, UserResponse

router = APIRouter(tags=["auth"])


@router.post("/register", status_code=201, response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if user_crud.get_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed = hash_password(user.password)
    db_user = user_crud.create(db, username=user.username, hashed_password=hashed)
    return db_user


@router.post("/login", response_model=Token)
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = user_crud.get_by_username(db, username=form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.username})
    return Token(access_token=token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
