"""
Public API of the analysis module. Other modules import only from here.
"""

from app.modules.analysis.errors import AnalysisFailed
from app.modules.analysis.parameters import PARAMETERS, Parameter
from app.modules.analysis.schemas import (
    AnalysisResult,
    LogoAnalysis,
    NotALogo,
    ParameterResult,
    Similarity,
)
from app.modules.analysis.service import analyze_logo

__all__ = [
    "analyze_logo",
    "AnalysisResult",
    "LogoAnalysis",
    "NotALogo",
    "ParameterResult",
    "Similarity",
    "Parameter",
    "PARAMETERS",
    "AnalysisFailed",
]