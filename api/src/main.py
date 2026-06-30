import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import engine
from src.models.user import Base
from src.routers.concept import router as concept
from src.routers.concept_mastery import router as concept_mastery
from src.routers.learner_profile import router as profile_router
from src.routers.users import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(profile_router)
app.include_router(concept_mastery)
app.include_router(concept)


@app.get("/")
async def read_root() -> dict[str, str]:
    result = {
        "message": "Root API EndPoint",
        "envVAR": f"{os.getenv('app_DB_USER')}",
    }
    return result
