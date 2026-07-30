from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.orm import Session

from backend_app.api.v1 import admin, auth, items
from backend_app.core.config import settings
from backend_app.database import SessionLocal, engine
from backend_app.models.base import Base
from backend_app.models.role import Role


def seed_roles():
    db: Session = SessionLocal()
    existing = db.query(Role).first()
    if existing:
        db.close()
        return
    roles = [
        Role(id=1, name="admin", description="Full system access"),
        Role(id=2, name="manager", description="Can manage all items"),
        Role(id=3, name="user", description="Can manage own items"),
    ]
    db.add_all(roles)
    db.commit()
    db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_roles()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(items.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
