"""
Every error leaves the API in one shape:  {"error": {"code": "...", "message": "..."}}
Registered once in main.py with register_error_handlers(app).
"""

import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import AppError, app_error_handler

logger = logging.getLogger(__name__)


def _error(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    # Log only where the problem is, never the submitted values.
    logger.info("Invalid request: %s", [".".join(map(str, e["loc"])) for e in exc.errors()[:5]])
    return _error(422, "INVALID_REQUEST", "The request data is invalid.")


async def http_error_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    status = HTTPStatus(exc.status_code)
    return _error(status.value, status.name, status.phrase + ".")


async def unexpected_error_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unexpected error", exc_info=exc)
    return _error(500, "INTERNAL_ERROR", AppError.message)


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_error_handler)
    app.add_exception_handler(Exception, unexpected_error_handler)