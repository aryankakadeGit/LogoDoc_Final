"""
Recommendation endpoints. The browser sends back the analysis it received from /analyze;
LogoAnalysis re-validates it and recalculates everything the backend owns.

POST /api/logo/recommendations/ai-prompt          { analysis }  -> { prompt }
POST /api/logo/recommendations/designer           { analysis }  -> { recommendations, overall }
POST /api/logo/recommendations/designer/download  { analysis, recommendations }  -> .txt (no AI)
"""

from fastapi import APIRouter, Response
from pydantic import BaseModel

from app.api.dependencies import AIDep
from app.api.rate_limit import rate_limited
from app.modules.analysis import LogoAnalysis
from app.modules.recommendations.ai_generated import ImprovedPrompt, generate_improved_prompt
from app.modules.recommendations.manual_design import (
    FILENAME,
    DesignerRecommendations,
    build_txt,
    generate_designer_recommendations,
)

router = APIRouter(prefix="/logo/recommendations", tags=["recommendations"])


class RecommendationRequest(BaseModel):
    analysis: LogoAnalysis


class DownloadRequest(BaseModel):
    analysis: LogoAnalysis
    recommendations: DesignerRecommendations


@router.post("/ai-prompt", response_model=ImprovedPrompt, dependencies=[rate_limited("ai-prompt")])
async def ai_prompt(body: RecommendationRequest, ai: AIDep) -> ImprovedPrompt:
    return await generate_improved_prompt(body.analysis, ai)


@router.post(
    "/designer", response_model=DesignerRecommendations, dependencies=[rate_limited("designer")]
)
async def designer(body: RecommendationRequest, ai: AIDep) -> DesignerRecommendations:
    return await generate_designer_recommendations(body.analysis, ai)


@router.post("/designer/download", response_class=Response)
def designer_download(body: DownloadRequest) -> Response:
    return Response(
        content=build_txt(body.analysis, body.recommendations),
        media_type="text/plain; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{FILENAME}"'},
    )