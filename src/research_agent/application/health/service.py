from __future__ import annotations

from research_agent.application.health.schemas import HealthResponse


class HealthService:
    async def check(self) -> HealthResponse:
        return HealthResponse()

