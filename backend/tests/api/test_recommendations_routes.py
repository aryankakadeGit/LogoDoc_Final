import json

import pytest

from tests.api.conftest import error_code
from tests.fakes.fake_ai_provider import FakeAIProvider
from tests.recommendations.conftest import make_analysis

BASE = "/api/logo/recommendations"
PROMPT = json.dumps({"prompt": "A flat vector logo of a blue rounded tile with a white monogram. " * 2})
DESIGNER = json.dumps(
    {
        "recommendations": [
            {
                "parameter_key": "typography",
                "problem": "Letters are tightly spaced.",
                "why_it_matters": "They blur at small sizes.",
                "suggestion": "Add letter spacing.",
                "preserve": "Keep the bold font.",
            }
        ],
        "overall": ["Remove the drop shadow."],
    }
)


def analysis_json(**scores) -> dict:
    return make_analysis(**({"default": 8, "typography": 5} | scores)).model_dump(mode="json")


def score_11() -> dict:
    data = analysis_json()
    data["parameters"][6]["score"] = 11  # colors
    return data


def test_ai_prompt(client_factory):
    ai = FakeAIProvider(PROMPT)
    response = client_factory(ai).post(f"{BASE}/ai-prompt", json={"analysis": analysis_json()})
    assert response.status_code == 200
    assert response.json()["prompt"].startswith("A flat vector logo")
    assert len(ai.calls) == 1 and ai.calls[0]["image_png"] is None


def test_designer(client_factory):
    response = client_factory(FakeAIProvider(DESIGNER)).post(
        f"{BASE}/designer", json={"analysis": analysis_json()}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["recommendations"][0]["key"] == "typography"
    assert body["recommendations"][0]["name"] == "Typography"
    assert body["overall"] == ["Remove the drop shadow."]


def test_tampered_overall_score_is_recalculated_before_the_ai_sees_it(client_factory):
    ai = FakeAIProvider(PROMPT)
    data = analysis_json()
    data["overall_score"] = 9.9
    client_factory(ai).post(f"{BASE}/ai-prompt", json={"analysis": data})
    assert "Overall score: 7.7/10" in ai.calls[0]["prompt"]  # (10*8 + 5) / 11


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"analysis": {"overall_score": 5}},
        {"analysis": score_11()},
    ],
)
def test_invalid_analysis_rejected_without_ai_call(client_factory, payload):
    ai = FakeAIProvider(PROMPT)
    response = client_factory(ai).post(f"{BASE}/ai-prompt", json=payload)
    assert (response.status_code, error_code(response)) == (422, "INVALID_REQUEST")
    assert ai.calls == []


def test_malformed_json_rejected(client_factory):
    response = client_factory().post(
        f"{BASE}/designer", content=b"{not json", headers={"content-type": "application/json"}
    )
    assert (response.status_code, error_code(response)) == (422, "INVALID_REQUEST")


def test_download_txt(client_factory):
    client = client_factory(FakeAIProvider(DESIGNER))
    analysis = analysis_json()
    recs = client.post(f"{BASE}/designer", json={"analysis": analysis}).json()

    response = client.post(f"{BASE}/designer/download", json={"analysis": analysis, "recommendations": recs})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    assert response.headers["content-disposition"] == 'attachment; filename="designer-recommendations.txt"'
    assert response.text.startswith("LOGO ANALYSIS - DESIGNER RECOMMENDATIONS")
    assert "What to change: Add letter spacing." in response.text


def test_download_rejects_invalid_recommendations(client_factory):
    bad = {"recommendations": [{"key": "not_a_parameter"}], "overall": []}
    response = client_factory().post(
        f"{BASE}/designer/download", json={"analysis": analysis_json(), "recommendations": bad}
    )
    assert (response.status_code, error_code(response)) == (422, "INVALID_REQUEST")


def test_each_ai_endpoint_has_its_own_limit_and_download_has_none(client_factory):
    client = client_factory(FakeAIProvider(PROMPT), rate_limit_analyze="1/minute")
    body = {"analysis": analysis_json()}
    assert client.post(f"{BASE}/ai-prompt", json=body).status_code == 200
    assert client.post(f"{BASE}/ai-prompt", json=body).status_code == 429
    assert client.post(f"{BASE}/designer", json=body).status_code != 429  # separate counter
    download = {"analysis": analysis_json(), "recommendations": {"recommendations": [], "overall": []}}
    assert all(
        client.post(f"{BASE}/designer/download", json=download).status_code == 200 for _ in range(3)
    )