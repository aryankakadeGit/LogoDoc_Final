"""
Custom application exceptions and their mapping to clean API error responses.
"""
"""
Base application error and its mapping to one clean JSON error response.

Modules define their own errors by subclassing AppError and setting
code / status_code / message. The API never leaks internal details.
"""

from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    code: str = "INTERNAL_ERROR"
    status_code: int = 500
    message: str = "Something went wrong. Please try again."

    def __init__(self, message: str | None = None) -> None:
        if message is not None:
            self.message = message
        super().__init__(self.message)


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    """Registered in main.py: AppError -> {"error": {"code", "message"}}."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )