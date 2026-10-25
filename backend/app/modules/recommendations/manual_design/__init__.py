"""
Public API of recommendations.manual_design.
"""

from app.modules.recommendations.manual_design.schemas import (
    DesignerRecommendation,
    DesignerRecommendations,
)
from app.modules.recommendations.manual_design.service import generate_designer_recommendations
from app.modules.recommendations.manual_design.txt_builder import FILENAME, build_txt

__all__ = [
    "generate_designer_recommendations",
    "build_txt",
    "FILENAME",
    "DesignerRecommendation",
    "DesignerRecommendations",
]