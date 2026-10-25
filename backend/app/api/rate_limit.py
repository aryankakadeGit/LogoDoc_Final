"""
Simple in-memory, per-IP sliding-window rate limit for the AI endpoints.
Limit comes from settings (e.g. "10/minute"). Each endpoint ("scope") has its own counter.

Note: in-memory = per server process. Behind a reverse proxy, run uvicorn with
--proxy-headers so request.client.host is the real user IP.
"""

import time
from collections import defaultdict, deque

from fastapi import Depends, Request

from app.api.dependencies import SettingsDep
from app.core.exceptions import AppError

_PERIOD_SECONDS = {"second": 1, "minute": 60, "hour": 3600, "day": 86400}


class RateLimited(AppError):
    code = "RATE_LIMITED"
    status_code = 429
    message = "Too many requests. Please wait a minute and try again."


class DailyQuotaReached(AppError):
    code = "DAILY_QUOTA_REACHED"
    status_code = 429
    message = "The free daily analysis limit has been reached. Please try again tomorrow."


def parse_limit(limit: str) -> tuple[int, int]:
    """'10/minute' -> (10, 60). The format is already validated by core config."""
    count, period = limit.split("/")
    return int(count), _PERIOD_SECONDS[period]


class RateLimiter:
    def __init__(self) -> None:
        self._hits: dict[tuple[str, str], deque[float]] = defaultdict(deque)

    def allow(self, key: tuple[str, str], limit: int, period: int, now: float | None = None) -> bool:
        now = time.monotonic() if now is None else now
        hits = self._hits[key]
        while hits and hits[0] <= now - period:
            hits.popleft()
        if len(hits) >= limit:
            return False
        hits.append(now)
        return True


def rate_limited(scope: str):
    """Route dependency: Depends(rate_limited("analyze"))."""

    def check(request: Request, settings: SettingsDep) -> None:
        limiter: RateLimiter = request.app.state.rate_limiter
        ip = request.client.host if request.client else "unknown"
        limit, period = parse_limit(settings.rate_limit_analyze)
        if not limiter.allow((scope, ip), limit, period):
            raise RateLimited()
        # One shared counter for every AI endpoint and every visitor (free-tier quota guard).
        if settings.ai_daily_limit and not limiter.allow(("ai-total", "*"), settings.ai_daily_limit, 86400):
            raise DailyQuotaReached()

    return Depends(check)