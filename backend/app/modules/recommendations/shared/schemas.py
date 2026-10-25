"""
Compact view of an analysis used by both recommendation types.
"""

from pydantic import BaseModel


class FocusItem(BaseModel):
    key: str
    name: str
    score: float
    positives: list[str]
    negatives: list[str]


class AnalysisSummary(BaseModel):
    logo_description: str
    overall_score: float
    improve: list[FocusItem]  # weakest first
    keep: list[FocusItem]  # strongest first
    fine_tune_only: bool  # True when nothing scored below the "weak" threshold