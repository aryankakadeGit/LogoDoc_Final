"""
Creates the configured AI provider from settings. Called once at startup (main.py),
so a missing key or model stops the app immediately with a clear message.
To add a provider later: implement AIProvider and branch on settings.ai_provider here.
"""

from app.core.config import Settings
from app.modules.ai.base import AIProvider
from app.modules.ai.errors import AIConfigError
from app.modules.ai.gemini_provider import GeminiProvider


def create_provider(settings: Settings) -> AIProvider:
    api_key = settings.gemini_api_key.get_secret_value()
    if not api_key:
        raise AIConfigError("GEMINI_API_KEY is not set in backend/.env")
    if not settings.gemini_model:
        raise AIConfigError("GEMINI_MODEL is not set in backend/.env")
    return GeminiProvider(api_key=api_key, model=settings.gemini_model)