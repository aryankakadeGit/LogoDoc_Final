"""
Recommendation errors. Messages are safe to show to the user.
"""

from app.core.exceptions import AppError


class RecommendationFailed(AppError):
    code = "RECOMMENDATION_FAILED"
    status_code = 502
    message = "We couldn't generate recommendations right now. Please try again."