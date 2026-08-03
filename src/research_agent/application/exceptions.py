from __future__ import annotations

from research_agent.core.exceptions import AppError


class ApplicationServiceError(AppError):
    code = "application_service_error"
    status_code = 500

