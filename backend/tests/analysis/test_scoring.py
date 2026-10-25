import pytest

from app.modules.analysis.scoring import overall_score, round_score


@pytest.mark.parametrize(
    "value, expected",
    [(8.25, 8.3), (8.24, 8.2), (8.35, 8.4), (7.05, 7.1), (10, 10.0), (0, 0.0), (6.666, 6.7)],
)
def test_round_half_up(value, expected):
    assert round_score(value) == expected


def test_simple_average():
    assert overall_score([8, 7, 9]) == 8.0


def test_not_applicable_scores_are_excluded():
    assert overall_score([8, None, 6, None]) == 7.0


def test_average_uses_the_rounded_scores_the_user_sees():
    # User sees 5.1, 5.1, 5.0 -> (15.2 / 3 = 5.07) -> 5.1.
    # Averaging the raw values instead would give 15.14 / 3 = 5.047 -> 5.0, which looks wrong on screen.
    assert overall_score([5.05, 5.05, 5.04]) == 5.1


def test_eleven_parameter_example():
    scores = [8.5, 7.5, 9, 6, 7, 5, 9, 8, 7.5, 6.5, 8]
    assert overall_score(scores) == 7.5  # 82 / 11 = 7.4545... -> 7.5


def test_no_applicable_scores_is_an_error():
    with pytest.raises(ValueError):
        overall_score([None, None])