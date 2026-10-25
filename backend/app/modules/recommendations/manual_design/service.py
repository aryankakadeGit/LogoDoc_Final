"""
"Manually Designed" recommendation: one text-only AI call that writes advice for a human designer.
Uses the existing analysis; the image is not analysed again.
"""

from app.modules.ai import AIProvider
from app.modules.analysis import LogoAnalysis
from app.modules.recommendations.manual_design.prompts import build_prompt
from app.modules.recommendations.manual_design.schemas import (
    AIDesignerResponse,
    DesignerRecommendation,
    DesignerRecommendations,
)
from app.modules.recommendations.shared import generate_validated, summarize, summary_text


async def generate_designer_recommendations(
    analysis: LogoAnalysis, ai: AIProvider
) -> DesignerRecommendations:
    summary = summarize(analysis)
    improve = {item.key: item for item in summary.improve}

    response = await generate_validated(
        ai,
        build_prompt(summary_text(summary)),
        AIDesignerResponse,
        context={"allowed_keys": list(improve)},
    )

    advice_by_key = {r.parameter_key: r for r in response.recommendations}
    recommendations = [
        DesignerRecommendation(
            key=key,
            name=item.name,
            score=item.score,
            **advice_by_key[key].model_dump(exclude={"parameter_key"}),
        )
        for key, item in improve.items()  # weakest first, as in the summary
        if key in advice_by_key
    ]
    return DesignerRecommendations(recommendations=recommendations, overall=response.overall)