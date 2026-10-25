"""
Entry point for the logo status check.
MVP uses only the AI analysis (no extra call). A future checker (e.g. Google Cloud Vision
logo/web detection) would be added here and its findings merged into the same LogoStatus.
"""

from app.modules.analysis import LogoAnalysis
from app.modules.logo_status.ai_checker import status_from_similarity
from app.modules.logo_status.schemas import LogoStatus


def get_logo_status(analysis: LogoAnalysis) -> LogoStatus:
    return status_from_similarity(analysis.similarity)