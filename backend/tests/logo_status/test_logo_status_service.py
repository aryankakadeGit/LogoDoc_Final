from app.modules.analysis import LogoAnalysis, ParameterResult, Similarity
from app.modules.analysis.parameters import PARAMETER_KEYS
from app.modules.logo_status import LogoStatus, get_logo_status


def test_uses_similarity_from_the_existing_analysis():
    analysis = LogoAnalysis(
        logo_description="The Google G.",
        parameters=[
            ParameterResult(key=k, score=8, positives=["ok"], negatives=[]) for k in PARAMETER_KEYS
        ],
        similarity=Similarity(match_level="exact_or_near_exact", recognized_brand="Google"),
    )
    status = get_logo_status(analysis)
    assert isinstance(status, LogoStatus)
    assert status.status == "matches_known_logo"
    assert status.recognized_brand == "Google"