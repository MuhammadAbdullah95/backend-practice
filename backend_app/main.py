from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend_app.api.v1 import auth, items
from backend_app.core.config import settings
from backend_app.database import engine
from backend_app.models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(items.router, prefix="/api/v1")
