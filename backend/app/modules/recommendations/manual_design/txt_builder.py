"""
Builds the downloadable designer-recommendations .txt from data that already exists
(the analysis + the generated recommendations). No AI call.
"""

import textwrap

from app.modules.analysis import LogoAnalysis
from app.modules.recommendations.manual_design.schemas import DesignerRecommendations

FILENAME = "designer-recommendations.txt"
_WIDTH = 88


def _wrap(text: str, indent: str = "") -> str:
    return textwrap.fill(text, _WIDTH, initial_indent=indent, subsequent_indent=indent)


def _bullets(items: list[str]) -> list[str]:
    return [_wrap(f"- {item}").replace("\n", "\n  ") for item in items] or ["- None noted"]


def build_txt(analysis: LogoAnalysis, recs: DesignerRecommendations) -> str:
    advice = {r.key: r for r in recs.recommendations}
    title = "LOGO ANALYSIS - DESIGNER RECOMMENDATIONS"
    lines = [title, "=" * len(title), "", _wrap(f"Logo: {analysis.logo_description}"),
             f"Overall Score: {analysis.overall_score}/10"]

    for p in analysis.parameters:
        lines += ["", "", p.name.upper()]
        if p.score is None:
            lines.append(f"Score: N/A ({p.not_applicable_reason or 'not applicable'})")
            continue
        lines += [f"Score: {p.score}/10", "", "Strengths:", *_bullets(p.positives),
                  "", "Areas for Improvement:", *_bullets(p.negatives), "", "Recommendation:"]
        a = advice.get(p.key)
        if a is None:
            lines.append("No major changes needed. Keep the strengths listed above.")
        else:
            lines += [
                _wrap(f"What is wrong: {a.problem}"),
                _wrap(f"Why it matters: {a.why_it_matters}"),
                _wrap(f"What to change: {a.suggestion}"),
                _wrap(f"What to keep: {a.preserve}"),
            ]

    heading = "OVERALL RECOMMENDATIONS"
    lines += ["", "", heading, "=" * len(heading), ""]
    lines += [_wrap(f"{i}. {text}").replace("\n", "\n   ") for i, text in enumerate(recs.overall, 1)]
    return "\n".join(lines) + "\n"