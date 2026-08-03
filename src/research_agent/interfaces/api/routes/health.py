from __future__ import annotations

from fastapi import APIRouter

from research_agent.application.health import HealthResponse
from research_agent.interfaces.api.dependencies import HealthServiceDep

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health(service: HealthServiceDep) -> HealthResponse:
    return await service.check()

