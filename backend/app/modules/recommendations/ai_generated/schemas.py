"""
Improved image-generation prompt (also the JSON shape the AI must return).
"""

from typing import Annotated

from pydantic import BaseModel, StringConstraints


class ImprovedPrompt(BaseModel):
    prompt: Annotated[str, StringConstraints(strip_whitespace=True, min_length=50, max_length=2500)]