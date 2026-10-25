"""
Builds a test app with the real routes + error handlers, a fake AI and test settings.
(main.py does the same wiring for the real app.)
"""

import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import RateLimiter, api_router, register_error_handlers
from app.core.config import Settings, get_settings
from tests.analysis.conftest import make_ai_data
from tests.fakes.fake_ai_provider import FakeAIProvider


def build_client(ai=None, *, with_ai: bool = True, **settings) -> TestClient:
    app = FastAPI()
    register_error_handlers(app)
    app.include_router(api_router)
    if with_ai:
        app.state.ai = ai or FakeAIProvider(json.dumps(make_ai_data()))
    app.state.rate_limiter = RateLimiter()
    test_settings = Settings(_env_file=None, **settings)
    app.dependency_overrides[get_settings] = lambda: test_settings
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def client_factory():
    return build_client


def error_code(response) -> str:
    return response.json()["error"]["code"]