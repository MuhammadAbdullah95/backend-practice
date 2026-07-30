from pydantic import BaseModel

from backend_app.schemas.role import RoleResponse


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    role: RoleResponse | None = None

    class Config:
        from_attributes = True


class UserRoleUpdate(BaseModel):
    role_id: int
