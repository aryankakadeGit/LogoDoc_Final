"""
One text-only AI call validated against a schema, with one retry if the output is invalid.
Used by both recommendation types.
"""

import logging
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

from app.modules.ai import AIProvider
from app.modules.recommendations.shared.errors import RecommendationFailed

logger = logging.getLogger(__name__)

MAX_ATTEMPTS = 2
M = TypeVar("M", bound=BaseModel)


async def generate_validated(
    ai: AIProvider, prompt: str, schema: type[M], context: dict[str, Any] | None = None
) -> M:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        text = await ai.generate_json(prompt, schema)
        try:
            return schema.model_validate_json(text, context=context)
        except ValidationError as exc:
            logger.warning(
                "Invalid AI %s (attempt %d/%d): %d problem(s)",
                schema.__name__, attempt, MAX_ATTEMPTS, exc.error_count(),
            )
    raise RecommendationFailed()