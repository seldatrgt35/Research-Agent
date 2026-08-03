from __future__ import annotations

import json
import logging
from logging.config import dictConfig
from typing import Any

from research_agent.core.config import LoggingSettings


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str)


def configure_logging(settings: LoggingSettings) -> None:
    formatter_name = "json" if settings.format == "json" else "plain"

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "plain": {
                    "format": "%(asctime)s %(levelname)s [%(name)s] %(message)s",
                },
                "json": {
                    "()": "research_agent.core.logging.JsonFormatter",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": formatter_name,
                },
            },
            "root": {
                "handlers": ["console"],
                "level": settings.level,
            },
            "loggers": {
                "uvicorn.access": {
                    "handlers": ["console"],
                    "level": settings.level,
                    "propagate": False,
                },
            },
        }
    )

