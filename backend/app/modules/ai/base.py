"""
AIProvider interface. The rest of the app depends only on this, so providers can be swapped.
"""

from typing import Protocol

from pydantic import BaseModel


class AIProvider(Protocol):
    async def generate_json(
        self, prompt: str, schema: type[BaseModel], image_png: bytes | None = None
    ) -> str:
        """Send the prompt (and optional PNG image); return the AI's raw JSON text.

        The schema tells the AI what JSON shape to produce. The caller must still
        parse and validate the returned text: the AI is never trusted blindly.
        Raises one of the errors in app.modules.ai.errors.
        """
        ...