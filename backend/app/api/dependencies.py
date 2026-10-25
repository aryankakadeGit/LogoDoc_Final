"""
Shared route dependencies. Tests replace these through app.dependency_overrides / app.state.
"""

from typing import Annotated

from fastapi import Depends, Request

from app.core.config import Settings, get_settings
from app.modules.ai import AIConfigError, AIProvider


def get_ai(request: Request) -> AIProvider:
    """The AI provider is created once at startup (main.py) and stored on app.state."""
    ai = getattr(request.app.state, "ai", None)
    if ai is None:
        raise AIConfigError()
    return ai


SettingsDep = Annotated[Settings, Depends(get_settings)]
AIDep = Annotated[AIProvider, Depends(get_ai)]