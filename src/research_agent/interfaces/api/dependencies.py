from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Annotated, cast

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from research_agent.application.health import HealthService
from research_agent.core.config import Settings
from research_agent.infrastructure.database.session import provide_session


def get_settings(request: Request) -> Settings:
    return cast(Settings, request.app.state.settings)


def get_health_service() -> HealthService:
    return HealthService()


async def get_db_session(request: Request) -> AsyncIterator[AsyncSession]:
    session_factory = cast(
        async_sessionmaker[AsyncSession],
        request.app.state.db_session_factory,
    )

    async for session in provide_session(session_factory):
        yield session


SettingsDep = Annotated[Settings, Depends(get_settings)]
HealthServiceDep = Annotated[HealthService, Depends(get_health_service)]
DatabaseSessionDep = Annotated[AsyncSession, Depends(get_db_session)]

