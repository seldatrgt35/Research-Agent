from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class AppError(Exception):
    code = "app_error"
    status_code = 500

    def __init__(
        self,
        message: str | None = None,
        *,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        self.message = message or "Application error"
        self.details = dict(details or {})
        super().__init__(self.message)


class ConfigurationError(AppError):
    code = "configuration_error"
    status_code = 500
