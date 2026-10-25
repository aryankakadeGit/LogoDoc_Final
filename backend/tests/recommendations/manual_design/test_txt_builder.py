from app.modules.recommendations.manual_design import (
    FILENAME,
    DesignerRecommendation,
    DesignerRecommendations,
    build_txt,
)

RECS = DesignerRecommendations(
    recommendations=[
        DesignerRecommendation(
            key="typography",
            name="Typography",
            score=5.0,
            problem="The wordmark letters are tightly spaced.",
            why_it_matters="Tight spacing blurs letters at small sizes.",
            suggestion="Add 5-10% letter spacing.",
            preserve="Keep the bold geometric font.",
        )
    ],
    overall=["Remove the drop shadow.", "Add spacing between icon and wordmark."],
)


def test_txt_layout_matches_spec(analysis):
    txt = build_txt(analysis(default=8, typography=5), RECS)
    assert txt.startswith("LOGO ANALYSIS - DESIGNER RECOMMENDATIONS\n=====")
    assert "Overall Score: 7.7/10" in txt  # (10*8 + 5) / 11
    assert "\n\nTYPOGRAPHY\nScore: 5.0/10\n\nStrengths:\n- typography strength\n" in txt
    assert "Areas for Improvement:\n- typography problem\n" in txt
    assert "What to change: Add 5-10% letter spacing." in txt
    assert "What to keep: Keep the bold geometric font." in txt
    assert "OVERALL RECOMMENDATIONS\n=======================\n\n1. Remove the drop shadow.\n2. Add" in txt
    assert txt.endswith("\n")


def test_every_parameter_is_listed_and_strong_ones_need_no_change(analysis):
    txt = build_txt(analysis(default=8, typography=5), RECS)
    for name in ("VISUAL SIMPLICITY", "COLORS", "TECHNICAL QUALITY"):
        assert f"\n{name}\n" in txt
    assert txt.count("No major changes needed.") == 10


def test_not_applicable_parameters_are_marked(analysis):
    txt = build_txt(analysis(default=8, typography=None, legibility=None), RECS)
    assert "TYPOGRAPHY\nScore: N/A (not applicable)" in txt


def test_long_lines_are_wrapped(analysis):
    long = DesignerRecommendations(recommendations=[], overall=["word " * 60])
    txt = build_txt(analysis(), long)
    assert max(len(line) for line in txt.splitlines()) <= 88


def test_filename():
    assert FILENAME.endswith(".txt")