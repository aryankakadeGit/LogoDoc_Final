"""
The real app from main.py: startup wiring, CORS, JSON size limit, error shape.
"""

import io
import json
import os

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.api.body_limit import MAX_JSON_BYTES
from app.core.config import Settings, get_settings
from app.main import create_app
from app.modules.ai import AIConfigError
from app.modules.ai.gemini_provider import GeminiProvider
from tests.analysis.conftest import make_ai_data
from tests.fakes.fake_ai_provider import FakeAIProvider

ORIGIN = "http://localhost:5173"


def settings(**values) -> Settings:
    base = {"gemini_api_key": "test-key", "gemini_model": "test-model", "cors_origins": ORIGIN}
    return Settings(_env_file=None, **(base | values))


@pytest.fixture
def client():
    s = settings()
    app = create_app(s)
    app.dependency_overrides[get_settings] = lambda: s
    with TestClient(app, raise_server_exceptions=False) as c:  # "with" runs startup
        c.app.state.ai = FakeAIProvider(json.dumps(make_ai_data()))  # never call real Gemini in tests
        yield c


def test_startup_creates_ai_provider_and_rate_limiter():
    with TestClient(create_app(settings())) as c:
        assert isinstance(c.app.state.ai, GeminiProvider)
        assert c.app.state.rate_limiter is not None
        assert c.get("/api/health").json() == {"status": "ok"}


@pytest.mark.parametrize("missing", ["gemini_api_key", "gemini_model"])
def test_startup_fails_clearly_without_key_or_model(missing):
    app = create_app(settings(**{missing: ""}))
    with pytest.raises(AIConfigError, match=missing.upper()):
        with TestClient(app):
            pass


def test_all_routes_are_mounted(client):
    paths = set(client.app.openapi()["paths"])
    assert paths == {
        "/api/health",
        "/api/logo/analyze",
        "/api/logo/recommendations/ai-prompt",
        "/api/logo/recommendations/designer",
        "/api/logo/recommendations/designer/download",
    }


def test_analyze_end_to_end(client, make_image):
    response = client.post("/api/logo/analyze", content=make_image("PNG"))
    assert response.status_code == 200
    assert response.json()["is_logo"] is True


def test_cors_allows_frontend_origin(client):
    response = client.options(
        "/api/logo/analyze",
        headers={"Origin": ORIGIN, "Access-Control-Request-Method": "POST"},
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ORIGIN


def test_cors_blocks_other_origins(client):
    response = client.get("/api/health", headers={"Origin": "http://evil.example"})
    assert "access-control-allow-origin" not in response.headers


def test_cors_exposes_download_filename(client):
    response = client.get("/api/health", headers={"Origin": ORIGIN})
    assert "content-disposition" in response.headers["access-control-expose-headers"].lower()


def test_large_json_body_rejected(client):
    big = {"analysis": {"logo_description": "x" * (300 * 1024)}}
    response = client.post("/api/logo/recommendations/ai-prompt", json=big)
    assert response.status_code == 413
    assert response.json()["error"]["code"] == "REQUEST_TOO_LARGE"


def test_large_chunked_json_body_rejected(client):
    def chunks():
        for _ in range(5):
            yield b"x" * (100 * 1024)

    response = client.post(
        "/api/logo/recommendations/designer",
        content=chunks(),
        headers={"content-type": "application/json"},
    )
    assert response.status_code == 413


def test_image_upload_is_not_limited_by_json_cap(client):
    noise = Image.frombytes("RGB", (400, 400), os.urandom(400 * 400 * 3))  # noise does not compress
    buf = io.BytesIO()
    noise.save(buf, "PNG")
    assert buf.tell() > MAX_JSON_BYTES
    assert client.post("/api/logo/analyze", content=buf.getvalue()).status_code == 200


def test_error_shape_is_installed(client):
    response = client.get("/api/does-not-exist")
    assert response.json()["error"]["code"] == "NOT_FOUND"