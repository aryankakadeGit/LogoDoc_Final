"""
Google Gemini implementation of AIProvider (google-genai SDK).

- Async, so the server is not blocked while waiting for the AI.
- 30 s timeout per attempt; up to 3 attempts, retried only for timeouts,
  connection errors and Google server errors (never for a bad key or used-up quota).
- Logs model, duration and error type only: never the key, image or response text.
"""

import logging
import time

import httpx
from google import genai
from google.genai import errors, types
from pydantic import BaseModel

from app.modules.ai.errors import AIBadResponse, AIConfigError, AIRateLimited, AIUnavailable

logger = logging.getLogger(__name__)

_TEMPERATURE = 0.2  # low = consistent scores for the same logo
_HTTP_OPTIONS = types.HttpOptions(
    timeout=30_000,  # milliseconds
    retry_options=types.HttpRetryOptions(attempts=3, http_status_codes=[408, 500, 502, 503, 504]),
)


class GeminiProvider:
    def __init__(self, api_key: str, model: str, client: genai.Client | None = None) -> None:
        self._model = model
        self._client = client or genai.Client(api_key=api_key, http_options=_HTTP_OPTIONS)

    async def generate_json(
        self, prompt: str, schema: type[BaseModel], image_png: bytes | None = None
    ) -> str:
        contents: list = [prompt]
        if image_png is not None:
            contents.insert(0, types.Part.from_bytes(data=image_png, mime_type="image/png"))
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
            temperature=_TEMPERATURE,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        )

        started = time.perf_counter()
        try:
            response = await self._client.aio.models.generate_content(
                model=self._model, contents=contents, config=config
            )
        except errors.APIError as exc:
            raise _map_api_error(exc) from exc
        except httpx.HTTPError as exc:
            logger.warning("AI request failed after retries: %s", type(exc).__name__)
            raise AIUnavailable() from exc

        finish_reason = response.candidates[0].finish_reason if response.candidates else None
        if not response.text or finish_reason not in (None, types.FinishReason.STOP):
            block_reason = response.prompt_feedback.block_reason if response.prompt_feedback else None
            logger.warning(
                "AI returned no usable output (finish_reason=%s, block_reason=%s)",
                finish_reason,
                block_reason,
            )
            raise AIBadResponse()

        logger.info("AI response from %s in %.1fs", self._model, time.perf_counter() - started)
        return response.text


def _map_api_error(exc: errors.APIError) -> Exception:
    logger.warning("AI API error %s %s: %s", exc.code, exc.status, exc.message)
    if exc.code == 429:
        return AIRateLimited()
    if exc.code in (400, 401, 403, 404):  # bad key, no access, unknown model, bad request
        return AIConfigError()
    return AIUnavailable()