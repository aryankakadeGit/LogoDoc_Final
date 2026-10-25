"""
Shared building blocks for the recommendation modules.
"""

from app.modules.recommendations.shared.ai_call import generate_validated
from app.modules.recommendations.shared.analysis_summary import summarize, summary_text
from app.modules.recommendations.shared.errors import RecommendationFailed
from app.modules.recommendations.shared.schemas import AnalysisSummary, FocusItem

__all__ = [
    "summarize",
    "summary_text",
    "generate_validated",
    "AnalysisSummary",
    "FocusItem",
    "RecommendationFailed",
]