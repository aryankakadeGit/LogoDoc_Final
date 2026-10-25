"""
Designer recommendations.
- AIDesignerResponse: what the AI must return (only for parameters it was asked to improve).
- DesignerRecommendations: the result; also accepted back from the browser for the .txt download.
"""

from typing import Annotated, Literal

from pydantic import BaseModel, Field, StringConstraints, ValidationInfo, model_validator

from app.modules.analysis.parameters import PARAMETER_KEYS

Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=600)]
ParameterKey = Literal[PARAMETER_KEYS]


class DesignerAdvice(BaseModel):
    problem: Text  # what is wrong
    why_it_matters: Text  # why it matters
    suggestion: Text  # what could be changed
    preserve: Text  # what should be kept


class AIDesignerItem(DesignerAdvice):
    parameter_key: ParameterKey


class AIDesignerResponse(BaseModel):
    recommendations: list[AIDesignerItem] = Field(min_length=1, max_length=len(PARAMETER_KEYS))
    overall: list[Text] = Field(min_length=1, max_length=5)

    @model_validator(mode="after")
    def _only_requested_parameters(self, info: ValidationInfo) -> "AIDesignerResponse":
        keys = [r.parameter_key for r in self.recommendations]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate parameter in recommendations")
        allowed = (info.context or {}).get("allowed_keys")
        if allowed is not None and not set(keys) <= set(allowed):
            raise ValueError("recommendation for a parameter that was not requested")
        return self


class DesignerRecommendation(DesignerAdvice):
    key: ParameterKey
    name: Annotated[str, StringConstraints(max_length=50)]
    score: Annotated[float, Field(ge=0, le=10)]


class DesignerRecommendations(BaseModel):
    recommendations: list[DesignerRecommendation] = Field(max_length=len(PARAMETER_KEYS))
    overall: list[Text] = Field(max_length=5)