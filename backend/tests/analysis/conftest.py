"""
Builders for AI analysis responses (as the AI would return them).
"""

import json

import pytest

from app.modules.analysis.parameters import PARAMETER_KEYS


def make_ai_data(score: float = 8.0, has_text: bool = True, **overrides) -> dict:
    data = {
        "is_logo": True,
        "has_text": has_text,
        "logo_description": "A blue square icon with the letters EO next to a bold black wordmark.",
        "parameters": {
            key: {"score": score, "positives": [f"{key} good"], "negatives": [f"{key} weak"]}
            for key in PARAMETER_KEYS
        },
        "similarity": {"recognized_brand": None, "match_level": "none", "notes": []},
    }
    data.update(overrides)
    return data


@pytest.fixture
def ai_data():
    return make_ai_data


@pytest.fixture
def to_json():
    return json.dumps