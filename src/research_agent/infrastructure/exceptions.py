from __future__ import annotations

from research_agent.core.exceptions import AppError


class InfrastructureError(AppError):
    code = "infrastructure_error"
    status_code = 502

