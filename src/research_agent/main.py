from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from research_agent.core.config import Settings
from research_agent.core.logging import configure_logging
from research_agent.infrastructure.database.session import (
    create_database_engine,
    create_session_factory,
)
from research_agent.interfaces.api.exception_handlers import register_exception_handlers
from research_agent.interfaces.api.router import api_router


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved_settings = settings or Settings()
    configure_logging(resolved_settings.logging)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        engine = create_database_engine(resolved_settings.database)
        app.state.settings = resolved_settings
        app.state.db_engine = engine
        app.state.db_session_factory = create_session_factory(engine)

        try:
            yield
        finally:
            await engine.dispose()

    app = FastAPI(
        title=resolved_settings.api.title,
        version=resolved_settings.api.version,
        debug=resolved_settings.debug,
        docs_url=resolved_settings.api.docs_url,
        redoc_url=resolved_settings.api.redoc_url,
        openapi_url=resolved_settings.api.openapi_url,
        lifespan=lifespan,
    )
    app.state.settings = resolved_settings

    app.include_router(api_router)
    register_exception_handlers(app)

    return app


app = create_app()

