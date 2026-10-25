"""
Tests for core.config
"""
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.core.config import Settings, get_settings

ENV_VARS = [
    "AI_PROVIDER",
    "GEMINI_API_KEY",
    "GEMINI_MODEL",
    "MAX_UPLOAD_MB",
    "MAX_IMAGE_DIMENSION",
    "RATE_LIMIT_ANALYZE",
    "CORS_ORIGINS",
    "LOG_LEVEL",
]


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """Tests must not depend on the developer's real environment or .env file."""
    for name in ENV_VARS:
        monkeypatch.delenv(name, raising=False)


def load(**overrides) -> Settings:
    return Settings(_env_file=None, **overrides)


def test_defaults():
    s = load()
    assert s.ai_provider == "gemini"
    assert s.gemini_api_key.get_secret_value() == ""
    assert s.gemini_model == ""
    assert s.max_upload_mb == 5
    assert s.max_upload_bytes == 5 * 1024 * 1024
    assert s.max_image_dimension == 2048
    assert s.rate_limit_analyze == "10/minute"
    assert s.cors_origins == ["http://localhost:5173"]
    assert s.log_level == "INFO"


def test_environment_variables_override_defaults(monkeypatch):
    monkeypatch.setenv("MAX_UPLOAD_MB", "8")
    monkeypatch.setenv("GEMINI_MODEL", "some-model")
    monkeypatch.setenv("LOG_LEVEL", "debug")
    s = load()
    assert (s.max_upload_mb, s.gemini_model, s.log_level) == (8, "some-model", "DEBUG")


def test_reads_env_file(tmp_path):
    env = tmp_path / ".env"
    env.write_text("GEMINI_API_KEY=abc123\nMAX_IMAGE_DIMENSION=1024\n", encoding="utf-8")
    s = Settings(_env_file=env)
    assert s.gemini_api_key.get_secret_value() == "abc123"
    assert s.max_image_dimension == 1024


def test_empty_values_in_env_file_use_defaults(tmp_path):
    env = tmp_path / ".env"
    env.write_text("MAX_UPLOAD_MB=\nMAX_IMAGE_DIMENSION=\nLOG_LEVEL=\n", encoding="utf-8")
    s = Settings(_env_file=env)
    assert (s.max_upload_mb, s.max_image_dimension, s.log_level) == (5, 2048, "INFO")


def test_cors_origins_comma_separated(monkeypatch):
    monkeypatch.setenv("CORS_ORIGINS", " http://a.com , http://b.com ,, ")
    assert load().cors_origins == ["http://a.com", "http://b.com"]


def test_api_key_is_hidden():
    s = load(gemini_api_key="super-secret-key")
    assert "super-secret-key" not in repr(s)
    assert "super-secret-key" not in str(s)
    assert "super-secret-key" not in s.model_dump_json()


@pytest.mark.parametrize(
    "name, value",
    [
        ("MAX_UPLOAD_MB", "0"),
        ("MAX_UPLOAD_MB", "-1"),
        ("MAX_UPLOAD_MB", "five"),
        ("MAX_IMAGE_DIMENSION", "0"),
        ("LOG_LEVEL", "LOUD"),
        ("AI_PROVIDER", "openai"),
        ("RATE_LIMIT_ANALYZE", "ten per minute"),
        ("RATE_LIMIT_ANALYZE", "10/week"),
    ],
)
def test_invalid_values_rejected(monkeypatch, name, value):
    monkeypatch.setenv(name, value)
    with pytest.raises(ValidationError):
        load()


def test_get_settings_is_cached():
    get_settings.cache_clear()
    assert get_settings() is get_settings()
    get_settings.cache_clear()


def test_env_example_template_is_valid():
    template = Path(__file__).parents[2] / ".env.example"
    s = Settings(_env_file=template)
    assert s.max_upload_mb == 5 and s.log_level == "INFO"