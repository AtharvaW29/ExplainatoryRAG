import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import engine
from src.models.user import Base
from src.routers.users import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)


@app.get("/")
async def read_root() -> dict[str, str]:
    result = {
        "message": "Root API EndPoint",
        "envVAR": f"{os.getenv('app_DB_USER')}",
    }
    return result
