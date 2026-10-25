import json

import pytest

from app.modules.ai import AIRateLimited, AIUnavailable
from tests.analysis.conftest import make_ai_data
from tests.api.conftest import error_code
from tests.fakes.fake_ai_provider import FakeAIProvider

URL = "/api/logo/analyze"


def test_logo_returns_analysis_and_logo_status(client_factory, make_image):
    ai = FakeAIProvider(json.dumps(make_ai_data(score=7)))
    response = client_factory(ai).post(URL, content=make_image("PNG", (40, 20)))

    assert response.status_code == 200
    body = response.json()
    assert body["is_logo"] is True
    assert body["analysis"]["overall_score"] == 7.0
    assert len(body["analysis"]["parameters"]) == 11
    assert body["logo_status"]["status"] == "no_significant_similarity"
    assert "not a trademark search" in body["logo_status"]["disclaimer"]
    assert len(ai.calls) == 1
    assert ai.calls[0]["image_png"].startswith(b"\x89PNG")


def test_svg_upload_works(client_factory):
    svg = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10"/></svg>'
    assert client_factory().post(URL, content=svg).status_code == 200


def test_not_a_logo(client_factory, make_image):
    ai = FakeAIProvider(json.dumps({"is_logo": False, "has_text": False}))
    body = client_factory(ai).post(URL, content=make_image("JPEG")).json()
    assert body["is_logo"] is False
    assert "logo" in body["message"]


@pytest.mark.parametrize(
    "content, status, code",
    [
        (b"", 400, "EMPTY_FILE"),
        (b"GIF89a....", 415, "UNSUPPORTED_FORMAT"),
        (b"\x89PNG\r\n\x1a\n" + b"broken" * 20, 422, "INVALID_IMAGE"),
        (b'<svg xmlns="http://www.w3.org/2000/svg"><image href="http://x/a.png"/></svg>', 422, "UNSAFE_SVG"),
    ],
)
def test_bad_uploads_never_reach_the_ai(client_factory, content, status, code):
    ai = FakeAIProvider()
    response = client_factory(ai).post(URL, content=content)
    assert (response.status_code, error_code(response)) == (status, code)
    assert ai.calls == []


def test_too_large_declared_size_rejected_before_reading(client_factory):
    ai = FakeAIProvider()
    response = client_factory(ai, max_upload_mb=1).post(URL, content=b"x" * (1024 * 1024 + 1))
    assert (response.status_code, error_code(response)) == (413, "FILE_TOO_LARGE")
    assert "1 MB" in response.json()["error"]["message"]
    assert ai.calls == []


def test_too_large_streamed_upload_without_size_header_is_stopped(client_factory):
    def chunks():  # chunked transfer: no Content-Length header
        for _ in range(3):
            yield b"x" * (600 * 1024)

    response = client_factory(max_upload_mb=1).post(URL, content=chunks())
    assert (response.status_code, error_code(response)) == (413, "FILE_TOO_LARGE")


@pytest.mark.parametrize(
    "error, status, code",
    [(AIRateLimited(), 429, "AI_RATE_LIMITED"), (AIUnavailable(), 503, "AI_UNAVAILABLE")],
)
def test_ai_errors_are_returned_in_error_shape(client_factory, make_image, error, status, code):
    response = client_factory(FakeAIProvider(error=error)).post(URL, content=make_image())
    assert (response.status_code, error_code(response)) == (status, code)


def test_invalid_ai_output_twice_is_analysis_failed(client_factory, make_image):
    response = client_factory(FakeAIProvider("not json")).post(URL, content=make_image())
    assert (response.status_code, error_code(response)) == (502, "ANALYSIS_FAILED")


def test_unexpected_error_is_generic_500(client_factory, make_image):
    response = client_factory(FakeAIProvider(error=RuntimeError("secret detail"))).post(
        URL, content=make_image()
    )
    assert (response.status_code, error_code(response)) == (500, "INTERNAL_ERROR")
    assert "secret detail" not in response.text


def test_missing_ai_provider_is_config_error(client_factory, make_image):
    response = client_factory(with_ai=False).post(URL, content=make_image())
    assert (response.status_code, error_code(response)) == (500, "AI_CONFIG_ERROR")


def test_rate_limit_per_ip(client_factory, make_image):
    client = client_factory(rate_limit_analyze="2/minute")
    codes = [client.post(URL, content=make_image()).status_code for _ in range(3)]
    assert codes == [200, 200, 429]
    assert error_code(client.post(URL, content=make_image())) == "RATE_LIMITED"