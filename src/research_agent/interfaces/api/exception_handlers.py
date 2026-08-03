from __future__ import annotations

from typing import cast

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from research_agent.core.exceptions import AppError


async def app_error_handler(_request: Request, exc: Exception) -> JSONResponse:
    app_error = cast(AppError, exc)

    return JSONResponse(
        status_code=app_error.status_code,
        content={
            "error": {
                "code": app_error.code,
                "message": app_error.message,
                "details": app_error.details,
            }
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
