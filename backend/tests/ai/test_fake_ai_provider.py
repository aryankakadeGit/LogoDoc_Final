import asyncio

import pytest
from pydantic import BaseModel

from app.modules.ai import AIProvider, AIUnavailable
from tests.fakes.fake_ai_provider import FakeAIProvider


class Answer(BaseModel):
    ok: bool


async def call(provider: AIProvider) -> str:
    return await provider.generate_json("prompt", Answer, b"png")


def test_fake_returns_canned_response_and_records_call():
    fake = FakeAIProvider(response='{"ok": true}')
    assert asyncio.run(call(fake)) == '{"ok": true}'
    assert fake.calls == [{"prompt": "prompt", "schema": Answer, "image_png": b"png"}]


def test_fake_can_raise_ai_errors():
    with pytest.raises(AIUnavailable):
        asyncio.run(call(FakeAIProvider(error=AIUnavailable())))