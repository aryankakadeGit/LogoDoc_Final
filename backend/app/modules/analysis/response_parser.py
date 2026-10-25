"""
Parses the AI's raw text into a validated AIAnalysisResponse.
Anything that is not valid JSON or breaks a rule raises InvalidAIOutput.
"""

from pydantic import ValidationError

from app.modules.analysis.schemas import AIAnalysisResponse


class InvalidAIOutput(Exception):
    """Internal: the AI's output broke the schema. The message is safe to log (no AI content)."""


def parse_ai_response(text: str) -> AIAnalysisResponse:
    try:
        return AIAnalysisResponse.model_validate_json(text)
    except ValidationError as exc:
        problems = "; ".join(
            f"{'.'.join(map(str, e['loc'])) or 'response'}: {e['type']}" for e in exc.errors()[:5]
        )
        raise InvalidAIOutput(f"{exc.error_count()} problem(s): {problems}") from exc