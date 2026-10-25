"""
Analysis errors. Messages are safe to show to the user.
"""

from app.core.exceptions import AppError


class AnalysisFailed(AppError):
    code = "ANALYSIS_FAILED"
    status_code = 502
    message = "We couldn't analyze this logo. Please try again."