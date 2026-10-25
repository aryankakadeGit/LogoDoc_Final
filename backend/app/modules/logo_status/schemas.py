"""
Logo status shown in the dashboard's first section.
"""

from typing import Literal

from pydantic import BaseModel

StatusLevel = Literal[
    "no_significant_similarity",  # nothing close to a known logo
    "generic_elements",  # only common shapes/styles; normal, not copying
    "potentially_similar",  # strong visual similarity to an existing logo
    "matches_known_logo",  # is, or nearly is, a known logo
]

DISCLAIMER = (
    "This is an automated visual check against well-known logos. "
    "It is not a trademark search or legal advice."
)


class LogoStatus(BaseModel):
    status: StatusLevel
    title: str
    message: str
    recognized_brand: str | None = None
    notes: list[str] = []
    sources_checked: list[str]
    disclaimer: str = DISCLAIMER