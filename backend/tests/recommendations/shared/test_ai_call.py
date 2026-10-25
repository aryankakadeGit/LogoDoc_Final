import asyncio

import pytest
from pydantic import BaseModel

from app.modules.ai import AIUnavailable
from app.modules.recommendations.shared import RecommendationFailed, generate_validated
from tests.fakes.fake_ai_provider import FakeAIProvider


class Out(BaseModel):
    text: str


class SequenceAI(FakeAIProvider):
    def __init__(self, *responses: str) -> None:
        super().__init__()
        self.responses = list(responses)

    async def generate_json(self, prompt, schema, image_png=None) -> str:
        self.response = self.responses[len(self.calls)]
        return await super().generate_json(prompt, schema, image_png)


def run(ai):
    return asyncio.run(generate_validated(ai, "prompt", Out))


def test_valid_first_time_is_one_text_only_call():
    ai = FakeAIProvider('{"text": "ok"}')
    assert run(ai) == Out(text="ok")
    assert ai.calls == [{"prompt": "prompt", "schema": Out, "image_png": None}]


def test_invalid_then_valid_retries_once():
    ai = SequenceAI("nope", '{"text": "ok"}')
    assert run(ai).text == "ok"
    assert len(ai.calls) == 2


def test_invalid_twice_fails():
    ai = SequenceAI("nope", "{}", "never used")
    with pytest.raises(RecommendationFailed):
        run(ai)
    assert len(ai.calls) == 2


def test_ai_errors_pass_through():
    with pytest.raises(AIUnavailable):
        run(FakeAIProvider(error=AIUnavailable()))