from app.modules.recommendations.shared import summarize, summary_text


def keys(items):
    return [i.key for i in items]


def test_weak_are_below_7_weakest_first_and_strong_are_8_plus(analysis):
    s = summarize(analysis(default=7.5, typography=5.5, colors=9, composition=6.9, memorability=8))
    assert keys(s.improve) == ["typography", "composition"]
    assert keys(s.keep) == ["colors", "memorability"]
    assert s.fine_tune_only is False


def test_score_of_exactly_7_is_not_weak_and_8_is_strong(analysis):
    s = summarize(analysis(default=7.0, colors=8.0, typography=6.9))
    assert keys(s.improve) == ["typography"]
    assert keys(s.keep) == ["colors"]


def test_all_strong_gives_two_fine_tune_items_not_also_kept(analysis):
    s = summarize(analysis(default=9, typography=8.1, colors=8.2))
    assert s.fine_tune_only is True
    assert keys(s.improve) == ["typography", "colors"]
    assert "typography" not in keys(s.keep) and "colors" not in keys(s.keep)


def test_not_applicable_parameters_are_skipped(analysis):
    s = summarize(analysis(default=6, typography=None, legibility=None))
    assert "typography" not in keys(s.improve) + keys(s.keep)
    assert len(s.improve) == 9


def test_ties_keep_parameter_order(analysis):
    s = summarize(analysis(default=8, scalability=5, colors=5))
    assert keys(s.improve) == ["scalability", "colors"]


def test_summary_carries_description_and_overall(analysis):
    s = summarize(analysis(default=6))
    assert s.overall_score == 6.0
    assert "ECOOPEX" in s.logo_description


def test_summary_text_is_tagged_and_lists_items(analysis):
    text = summary_text(summarize(analysis(default=7.5, typography=5.5, colors=9)))
    assert text.startswith("<logo_analysis>") and text.endswith("</logo_analysis>")
    assert "Areas to improve (weakest first):" in text
    assert "- Typography [typography] (5.5/10)" in text
    assert "Problems: typography problem" in text
    assert "- Colors (9.0/10): colors strength" in text


def test_summary_text_without_strong_items(analysis):
    text = summary_text(summarize(analysis(default=6)))
    assert "None scored 8 or above" in text


def test_summary_text_fine_tune_heading(analysis):
    text = summary_text(summarize(analysis(default=9)))
    assert "fine-tune these" in text