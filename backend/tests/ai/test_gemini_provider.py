import asyncio
import logging
from types import SimpleNamespace

import httpx
import pytest
from google.genai import errors, types
from pydantic import BaseModel

from app.modules.ai import gemini_provider
from app.modules.ai.errors import AIBadResponse, AIConfigError, AIRateLimited, AIUnavailable
from app.modules.ai.gemini_provider import GeminiProvider


class Answer(BaseModel):
    is_logo: bool


class FakeModels:
    """Stands in for client.aio.models; records the call, returns or raises."""

    def __init__(self, result):
        self.result = result
        self.kwargs = None

    async def generate_content(self, **kwargs):
        self.kwargs = kwargs
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


def response(text: str | None = '{"is_logo": true}', finish=types.FinishReason.STOP):
    if text is None:
        return types.GenerateContentResponse()
    return types.GenerateContentResponse(
        candidates=[
            types.Candidate(
                content=types.Content(parts=[types.Part(text=text)]), finish_reason=finish
            )
        ]
    )


def api_error(cls, code: int, status: str):
    return cls(code, {"error": {"code": code, "message": f"{status} details", "status": status}})


def run(result, prompt="Is this a logo?", image=b"\x89PNG-fake"):
    models = FakeModels(result)
    provider = GeminiProvider(
        api_key="unused", model="test-model", client=SimpleNamespace(aio=SimpleNamespace(models=models))
    )
    text = asyncio.run(provider.generate_json(prompt, Answer, image))
    return text, models.kwargs


def test_returns_raw_json_text():
    text, _ = run(response('{"is_logo": true}'))
    assert text == '{"is_logo": true}'


def test_sends_image_then_prompt_with_json_schema_config():
    _, kwargs = run(response(), prompt="Analyze", image=b"PNGDATA")
    assert kwargs["model"] == "test-model"
    image_part, prompt = kwargs["contents"]
    assert image_part.inline_data.data == b"PNGDATA"
    assert image_part.inline_data.mime_type == "image/png"
    assert prompt == "Analyze"
    config = kwargs["config"]
    assert config.response_mime_type == "application/json"
    assert config.response_schema is Answer
    assert config.temperature == 0.2
    assert config.automatic_function_calling.disable is True


def test_text_only_call_has_no_image_part():
    _, kwargs = run(response(), prompt="Write a prompt", image=None)
    assert kwargs["contents"] == ["Write a prompt"]


@pytest.mark.parametrize(
    "error, expected",
    [
        (api_error(errors.ClientError, 429, "RESOURCE_EXHAUSTED"), AIRateLimited),
        (api_error(errors.ClientError, 400, "INVALID_ARGUMENT"), AIConfigError),
        (api_error(errors.ClientError, 403, "PERMISSION_DENIED"), AIConfigError),
        (api_error(errors.ClientError, 404, "NOT_FOUND"), AIConfigError),
        (api_error(errors.ServerError, 500, "INTERNAL"), AIUnavailable),
        (api_error(errors.ServerError, 503, "UNAVAILABLE"), AIUnavailable),
        (httpx.ReadTimeout("timed out"), AIUnavailable),
        (httpx.ConnectError("no network"), AIUnavailable),
    ],
)
def test_errors_are_mapped(error, expected):
    with pytest.raises(expected):
        run(error)


@pytest.mark.parametrize(
    "result",
    [
        response(None),  # no candidates at all (e.g. prompt blocked)
        response(""),  # empty text
        response('{"is_logo": tr', finish=types.FinishReason.MAX_TOKENS),  # cut off
        response('{"is_logo": true}', finish=types.FinishReason.SAFETY),
    ],
)
def test_unusable_responses_rejected(result):
    with pytest.raises(AIBadResponse):
        run(result)


def test_logs_never_contain_prompt_image_or_response(caplog):
    caplog.set_level(logging.DEBUG)
    run(response('{"is_logo": "SECRET-ANSWER"}'), prompt="SECRET-PROMPT", image=b"SECRET-IMAGE")
    with pytest.raises(AIRateLimited):
        run(api_error(errors.ClientError, 429, "RESOURCE_EXHAUSTED"), prompt="SECRET-PROMPT")
    logs = caplog.text
    assert "test-model" in logs and "429" in logs
    assert "SECRET" not in logs


def test_retry_policy_never_retries_quota_or_bad_requests():
    retry = gemini_provider._HTTP_OPTIONS.retry_options
    assert retry.attempts == 3
    assert 429 not in retry.http_status_codes and 400 not in retry.http_status_codes
    assert gemini_provider._HTTP_OPTIONS.timeout == 30_000