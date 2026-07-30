from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend_app.api.v1 import admin, auth, items
from backend_app.core.config import settings
from backend_app.database import SessionLocal, engine
from backend_app.core.security import hash_password
from backend_app.models.base import Base
from backend_app.models.role import Role
from backend_app.models.user import User


def seed_db():
    db: Session = SessionLocal()

    if not db.query(Role).first():
        roles = [
            Role(id=1, name="admin", description="Full system access"),
            Role(id=2, name="manager", description="Can manage all items"),
            Role(id=3, name="user", description="Can manage own items"),
        ]
        db.add_all(roles)
        db.commit()

    if not db.query(User).filter(User.username == "admin").first():
        db.add(
            User(
                username="admin",
                hashed_password=hash_password("admin123"),
                role_id=1,
            )
        )
    if not db.query(User).filter(User.username == "manager").first():
        db.add(
            User(
                username="manager",
                hashed_password=hash_password("manager123"),
                role_id=2,
            )
        )
    db.commit()
    db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_db()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(items.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
