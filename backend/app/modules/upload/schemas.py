"""
Data structures for a validated, normalized image (bytes, mime type, original format, dimensions).
"""
"""
Upload module output.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

SourceFormat = Literal["png", "jpeg", "webp", "svg"]


class PreparedImage(BaseModel):
    """A safe, normalized PNG ready to send to the AI."""

    model_config = ConfigDict(frozen=True)

    png_bytes: bytes = Field(repr=False)
    width: int
    height: int
    source_format: SourceFormat