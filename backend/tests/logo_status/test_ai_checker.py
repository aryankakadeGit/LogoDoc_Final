import pytest

from app.modules.analysis import Similarity
from app.modules.logo_status.ai_checker import SOURCE, status_from_similarity
from app.modules.logo_status.schemas import DISCLAIMER


def check(match_level: str, brand: str | None = None, notes: list[str] | None = None):
    return status_from_similarity(
        Similarity(match_level=match_level, recognized_brand=brand, notes=notes or [])
    )


def test_exact_match_with_brand():
    s = check("exact_or_near_exact", "Google")
    assert s.status == "matches_known_logo"
    assert s.recognized_brand == "Google"
    assert "Google" in s.message


def test_exact_match_without_brand_is_only_potentially_similar():
    s = check("exact_or_near_exact", None)
    assert s.status == "potentially_similar"
    assert "an existing well-known logo" in s.message


def test_strong_similarity_names_brand_when_known():
    s = check("strong_similarity", "Nike")
    assert s.status == "potentially_similar"
    assert s.title == "Potentially similar logo detected"
    assert "the Nike logo" in s.message


def test_generic_elements_is_reassuring_and_hides_brand():
    s = check("generic_elements", "SomeBrand", ["Common app-tile shape"])
    assert s.status == "generic_elements"
    assert s.recognized_brand is None
    assert "does not mean it was copied" in s.message
    assert s.notes == ["Common app-tile shape"]


@pytest.mark.parametrize("brand", [None, "SomeBrand"])
def test_no_similarity_never_shows_a_brand(brand):
    s = check("none", brand)
    assert s.status == "no_significant_similarity"
    assert s.recognized_brand is None


def test_blank_brand_is_treated_as_unknown():
    assert check("exact_or_near_exact", "   ").status == "potentially_similar"


@pytest.mark.parametrize("level", ["none", "generic_elements", "strong_similarity", "exact_or_near_exact"])
def test_every_status_has_sources_and_disclaimer_and_no_originality_claim(level):
    s = check(level, "Brand")
    assert s.sources_checked == [SOURCE]
    assert s.disclaimer == DISCLAIMER
    assert "not a trademark search" in s.disclaimer
    text = f"{s.title} {s.message}".lower()
    assert "original" not in text and "infring" not in text