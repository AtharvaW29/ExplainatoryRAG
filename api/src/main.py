import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import engine
from src.graph.database import close_graph_driver
from src.graph.scripts.init_graph import initialize_graph
from src.models.user import Base
from src.routers.concept import router as concept
from src.routers.concept_mastery import router as concept_mastery
from src.routers.concept_relationship import router as concept_relationship
from src.routers.graph import router as graph_router
from src.routers.learner_profile import router as profile_router
from src.routers.misconception import router as misconception_router
from src.routers.users import router as user_router

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await initialize_graph()
    await close_graph_driver()
    logger.info("Both Databases Configured and Connected Successfully!")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(profile_router)
app.include_router(concept_mastery)
app.include_router(concept)
app.include_router(concept_relationship)
app.include_router(graph_router)
app.include_router(misconception_router)


@app.get("/")
async def read_root() -> dict[str, str]:
    result = {
        "message": "Root API EndPoint",
        "envVAR": f"{os.getenv('app_DB_USER')}",
    }
    return result
