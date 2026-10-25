"""
Logo analysis: one AI call -> strict validation (one retry if invalid) -> backend scoring.
"""

import logging

from app.modules.ai import AIProvider
from app.modules.analysis.errors import AnalysisFailed
from app.modules.analysis.parameters import PARAMETERS
from app.modules.analysis.prompts import ANALYSIS_PROMPT
from app.modules.analysis.response_parser import InvalidAIOutput, parse_ai_response
from app.modules.analysis.schemas import (
    AIAnalysisResponse,
    LogoAnalysis,
    NotALogo,
    ParameterResult,
)
from app.modules.analysis.scoring import round_score
from app.modules.upload import PreparedImage

logger = logging.getLogger(__name__)

MAX_ATTEMPTS = 2  # first try + one retry when the AI output is invalid
NO_TEXT_REASON = "Not applicable: this logo has no text."


async def analyze_logo(image: PreparedImage, ai: AIProvider) -> LogoAnalysis | NotALogo:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        text = await ai.generate_json(ANALYSIS_PROMPT, AIAnalysisResponse, image.png_bytes)
        try:
            parsed = parse_ai_response(text)
            break
        except InvalidAIOutput as exc:
            logger.warning("Invalid AI analysis (attempt %d/%d): %s", attempt, MAX_ATTEMPTS, exc)
    else:
        raise AnalysisFailed()

    if not parsed.is_logo:
        return NotALogo()
    return _build_analysis(parsed)


def _build_analysis(parsed: AIAnalysisResponse) -> LogoAnalysis:
    """Names, explanations and the overall score are filled in by LogoAnalysis itself."""
    results = []
    for p in PARAMETERS:
        assessment = getattr(parsed.parameters, p.key)
        if p.needs_text and not parsed.has_text:
            results.append(
                ParameterResult(
                    key=p.key, score=None, positives=[], negatives=[],
                    not_applicable_reason=NO_TEXT_REASON,
                )
            )
        else:
            results.append(
                ParameterResult(
                    key=p.key, score=round_score(assessment.score),
                    positives=assessment.positives, negatives=assessment.negatives,
                )
            )

    return LogoAnalysis(
        logo_description=parsed.logo_description,
        parameters=results,
        similarity=parsed.similarity,
    )