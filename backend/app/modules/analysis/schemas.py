"""
Two kinds of schema:
- AIAnalysisResponse: what the AI must return (also sent to the AI as its JSON schema).
- LogoAnalysis / NotALogo: the clean result this module returns to the rest of the app.

LogoAnalysis is also accepted back from the browser (for recommendations), so it validates
itself strictly and recalculates everything the backend owns (names, explanations, overall score).
"""

from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, Field, StringConstraints, create_model, model_validator

from app.modules.analysis.parameters import PARAMETER_KEYS, PARAMETERS
from app.modules.analysis.scoring import overall_score

MAX_POINTS = 3

Point = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=300)]
# Extra bullet points are harmless: keep the first MAX_POINTS instead of rejecting the analysis.
Points = Annotated[list[Point], BeforeValidator(lambda v: v[:MAX_POINTS] if isinstance(v, list) else v)]
Description = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=600)]
Score = Annotated[float, Field(ge=0, le=10)]

MatchLevel = Literal["none", "generic_elements", "strong_similarity", "exact_or_near_exact"]


# ---------- AI response ----------


class ParameterAssessment(BaseModel):
    score: Score | None = None
    positives: Points = []
    negatives: Points = []

    @model_validator(mode="after")
    def _has_feedback(self) -> "ParameterAssessment":
        if self.score is not None and not (self.positives or self.negatives):
            raise ValueError("a scored parameter needs at least one positive or negative")
        return self


AIParameters = create_model(
    "AIParameters", **{key: (ParameterAssessment, ...) for key in PARAMETER_KEYS}
)


class Similarity(BaseModel):
    recognized_brand: Annotated[str, StringConstraints(max_length=100)] | None = None
    match_level: MatchLevel
    notes: Points = []


class AIAnalysisResponse(BaseModel):
    is_logo: bool
    has_text: bool
    logo_description: Description | None = None
    parameters: AIParameters | None = None
    similarity: Similarity | None = None

    @model_validator(mode="after")
    def _complete_when_logo(self) -> "AIAnalysisResponse":
        if not self.is_logo:
            return self
        if self.logo_description is None or self.parameters is None or self.similarity is None:
            raise ValueError("logo_description, parameters and similarity are required for a logo")
        for p in PARAMETERS:
            applies = self.has_text or not p.needs_text
            if applies and getattr(self.parameters, p.key).score is None:
                raise ValueError(f"missing score for {p.key}")
        return self


# ---------- Result returned by this module ----------


class ParameterResult(BaseModel):
    key: str
    name: str = ""  # always set from PARAMETERS
    explanation: str = ""  # always set from PARAMETERS
    score: Score | None  # None = not applicable
    positives: Points
    negatives: Points
    not_applicable_reason: Annotated[str, StringConstraints(max_length=200)] | None = None


class LogoAnalysis(BaseModel):
    is_logo: Literal[True] = True
    overall_score: float = 0.0  # always recalculated by the backend
    logo_description: Description
    parameters: list[ParameterResult]
    similarity: Similarity

    @model_validator(mode="after")
    def _consistent(self) -> "LogoAnalysis":
        if [r.key for r in self.parameters] != list(PARAMETER_KEYS):
            raise ValueError("parameters must be the known parameters, in order")
        for result, param in zip(self.parameters, PARAMETERS, strict=True):
            if result.score is None and not param.needs_text:
                raise ValueError(f"{param.key} must have a score")
            result.name, result.explanation = param.name, param.explanation
        self.overall_score = overall_score(r.score for r in self.parameters)
        return self


class NotALogo(BaseModel):
    is_logo: Literal[False] = False
    message: str = "The uploaded image does not appear to be a logo. Please upload a valid logo image."


AnalysisResult = Annotated[LogoAnalysis | NotALogo, Field(discriminator="is_logo")]