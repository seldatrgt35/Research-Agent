from __future__ import annotations

from research_agent.core.exceptions import AppError


class DomainError(AppError):
    code = "domain_error"
    status_code = 422


class EntityNotFoundError(DomainError):
    code = "entity_not_found"
    status_code = 404

