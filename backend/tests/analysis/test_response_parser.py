import pytest

from app.modules.analysis.response_parser import InvalidAIOutput, parse_ai_response


def test_valid_response(ai_data, to_json):
    parsed = parse_ai_response(to_json(ai_data()))
    assert parsed.is_logo and parsed.parameters.colors.score == 8.0


def test_not_a_logo_needs_no_parameters():
    text = '{"is_logo": false, "has_text": false, "parameters": null, "similarity": null}'
    parsed = parse_ai_response(text)
    assert parsed.is_logo is False


def test_not_json_rejected():
    with pytest.raises(InvalidAIOutput):
        parse_ai_response("Sure! Here is the analysis: ...")


def test_missing_parameter_rejected(ai_data, to_json):
    data = ai_data()
    del data["parameters"]["colors"]
    with pytest.raises(InvalidAIOutput, match="colors"):
        parse_ai_response(to_json(data))


@pytest.mark.parametrize("bad", [17, -1, 10.5, "eight", None])
def test_bad_scores_rejected(ai_data, to_json, bad):
    data = ai_data()
    data["parameters"]["colors"]["score"] = bad
    with pytest.raises(InvalidAIOutput):
        parse_ai_response(to_json(data))


@pytest.mark.parametrize("edge", [0, 10, 7.5])
def test_edge_scores_accepted(ai_data, to_json, edge):
    data = ai_data()
    data["parameters"]["colors"]["score"] = edge
    assert parse_ai_response(to_json(data)).parameters.colors.score == edge


def test_logo_without_parameters_rejected(ai_data, to_json):
    with pytest.raises(InvalidAIOutput):
        parse_ai_response(to_json(ai_data(parameters=None)))


def test_text_scores_required_when_logo_has_text(ai_data, to_json):
    data = ai_data(has_text=True)
    data["parameters"]["typography"]["score"] = None
    with pytest.raises(InvalidAIOutput):
        parse_ai_response(to_json(data))


def test_text_scores_may_be_null_when_no_text(ai_data, to_json):
    data = ai_data(has_text=False)
    for key in ("typography", "legibility"):
        data["parameters"][key] = {"score": None, "positives": [], "negatives": []}
    assert parse_ai_response(to_json(data)).has_text is False


def test_scored_parameter_needs_feedback(ai_data, to_json):
    data = ai_data()
    data["parameters"]["colors"].update(positives=[], negatives=[])
    with pytest.raises(InvalidAIOutput):
        parse_ai_response(to_json(data))


def test_empty_negatives_allowed_if_positives_present(ai_data, to_json):
    data = ai_data()
    data["parameters"]["colors"]["negatives"] = []
    assert parse_ai_response(to_json(data)).parameters.colors.negatives == []


@pytest.mark.parametrize("point", ["", "   ", "x" * 301])
def test_bad_points_rejected(ai_data, to_json, point):
    data = ai_data()
    data["parameters"]["colors"]["positives"] = [point]
    with pytest.raises(InvalidAIOutput):
        parse_ai_response(to_json(data))


def test_points_trimmed_and_extra_points_dropped(ai_data, to_json):
    data = ai_data()
    data["parameters"]["colors"]["positives"] = ["  a  ", "b", "c", "d", "e"]
    assert parse_ai_response(to_json(data)).parameters.colors.positives == ["a", "b", "c"]


def test_unknown_match_level_rejected(ai_data, to_json):
    data = ai_data()
    data["similarity"]["match_level"] = "copied"
    with pytest.raises(InvalidAIOutput):
        parse_ai_response(to_json(data))


def test_unknown_extra_fields_ignored(ai_data, to_json):
    data = ai_data(overall_score=9.9, extra="ignored")
    assert not hasattr(parse_ai_response(to_json(data)), "overall_score")


def test_error_message_never_contains_ai_text(ai_data, to_json):
    data = ai_data()
    data["parameters"]["colors"]["score"] = "SECRET-AI-TEXT"
    with pytest.raises(InvalidAIOutput) as exc:
        parse_ai_response(to_json(data))
    assert "SECRET" not in str(exc.value)
    assert "parameters.colors.score" in str(exc.value)