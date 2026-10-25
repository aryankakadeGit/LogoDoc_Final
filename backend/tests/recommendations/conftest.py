"""
Builds a valid LogoAnalysis with chosen scores for recommendation tests.
"""

import pytest

from app.modules.analysis import LogoAnalysis, ParameterResult, Similarity
from app.modules.analysis.parameters import PARAMETER_KEYS


def make_analysis(default: float | None = 8.0, **scores: float | None) -> LogoAnalysis:
    return LogoAnalysis(
        logo_description="A blue rounded tile with the letters EO beside a bold black ECOOPEX wordmark.",
        parameters=[
            ParameterResult(
                key=key,
                score=scores.get(key, default),
                positives=[f"{key} strength"],
                negatives=[f"{key} problem"],
            )
            for key in PARAMETER_KEYS
        ],
        similarity=Similarity(match_level="none"),
    )


@pytest.fixture
def analysis():
    return make_analysis