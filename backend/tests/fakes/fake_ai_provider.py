"""
Fake AIProvider returning a canned response (or raising an error) so tests never use real AI quota.
"""

from pydantic import BaseModel


class FakeAIProvider:
    def __init__(self, response: str = "{}", error: Exception | None = None) -> None:
        self.response = response
        self.error = error
        self.calls: list[dict] = []

    async def generate_json(
        self, prompt: str, schema: type[BaseModel], image_png: bytes | None = None
    ) -> str:
        self.calls.append({"prompt": prompt, "schema": schema, "image_png": image_png})
        if self.error is not None:
            raise self.error
        return self.response