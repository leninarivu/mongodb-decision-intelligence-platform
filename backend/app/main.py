import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.knowledge import router as knowledge_router
from app.api.relationship_intelligence import router as relationship_intelligence_router
from app.api.workspace import router as workspace_router
from app.core.config import get_settings
from app.db.mongodb import close_mongodb, connect_mongodb


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await connect_mongodb()
    try:
        yield
    finally:
        await close_mongodb()


def create_app() -> FastAPI:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level.upper())
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(knowledge_router)
    app.include_router(relationship_intelligence_router)
    app.include_router(workspace_router)
    return app


app = create_app()
