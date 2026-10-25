"""
AI errors. Messages are safe to show to the user; technical details go to the logs.
"""

from app.core.exceptions import AppError


class AIConfigError(AppError):
    code = "AI_CONFIG_ERROR"
    status_code = 500
    message = "The AI service is not configured correctly."


class AIRateLimited(AppError):
    code = "AI_RATE_LIMITED"
    status_code = 429
    message = "The AI service is busy right now. Please try again in a minute."


class AIUnavailable(AppError):
    code = "AI_UNAVAILABLE"
    status_code = 503
    message = "The AI service is temporarily unavailable. Please try again."


class AIBadResponse(AppError):
    code = "AI_BAD_RESPONSE"
    status_code = 502
    message = "The AI returned an unusable response. Please try again."