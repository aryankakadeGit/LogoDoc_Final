"""
Public API of the api layer: the router, the error handlers and the rate limiter for main.py.
"""

from app.api.error_handlers import register_error_handlers
from app.api.rate_limit import RateLimiter
from app.api.router import api_router

__all__ = ["api_router", "register_error_handlers", "RateLimiter"]