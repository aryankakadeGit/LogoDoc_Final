import pytest

from app.core.config import Settings
from app.modules.ai import AIConfigError, create_provider
from app.modules.ai.gemini_provider import GeminiProvider


def settings(**values) -> Settings:
    return Settings(_env_file=None, **values)


def test_missing_key_rejected():
    with pytest.raises(AIConfigError, match="GEMINI_API_KEY"):
        create_provider(settings(gemini_api_key="", gemini_model="some-model"))


def test_missing_model_rejected():
    with pytest.raises(AIConfigError, match="GEMINI_MODEL"):
        create_provider(settings(gemini_api_key="key", gemini_model=""))


def test_valid_config_creates_gemini_provider_without_network():
    provider = create_provider(settings(gemini_api_key="key", gemini_model="some-model"))
    assert isinstance(provider, GeminiProvider)