"""
Picks what to improve and what to keep from an existing analysis (no AI), and renders it as a
compact text block for the recommendation prompts.
"""

from app.modules.analysis import LogoAnalysis, ParameterResult
from app.modules.recommendations.shared.schemas import AnalysisSummary, FocusItem

WEAK_BELOW = 7.0
STRONG_FROM = 8.0
FINE_TUNE_COUNT = 2


def _focus(p: ParameterResult) -> FocusItem:
    return FocusItem(
        key=p.key, name=p.name, score=p.score, positives=p.positives, negatives=p.negatives
    )


def summarize(analysis: LogoAnalysis) -> AnalysisSummary:
    scored = [p for p in analysis.parameters if p.score is not None]  # N/A parameters are skipped
    by_score = sorted(scored, key=lambda p: p.score)  # stable: ties keep parameter order

    weak = [p for p in by_score if p.score < WEAK_BELOW]
    improve = weak or by_score[:FINE_TUNE_COUNT]
    improve_keys = {p.key for p in improve}
    keep = [p for p in reversed(by_score) if p.score >= STRONG_FROM and p.key not in improve_keys]

    return AnalysisSummary(
        logo_description=analysis.logo_description,
        overall_score=analysis.overall_score,
        improve=[_focus(p) for p in improve],
        keep=[_focus(p) for p in keep],
        fine_tune_only=not weak,
    )


def summary_text(summary: AnalysisSummary) -> str:
    """Text block inserted into prompts. Wrapped in tags so the AI treats it as data."""
    heading = (
        "Already strong overall; fine-tune these (lowest first):"
        if summary.fine_tune_only
        else "Areas to improve (weakest first):"
    )
    lines = [
        "<logo_analysis>",
        f"Logo: {summary.logo_description}",
        f"Overall score: {summary.overall_score}/10",
        "",
        heading,
    ]
    for item in summary.improve:
        lines.append(f"- {item.name} [{item.key}] ({item.score}/10)")
        lines.append(f"  Problems: {'; '.join(item.negatives) or 'none listed'}")
        lines.append(f"  Working well: {'; '.join(item.positives) or 'none listed'}")
    lines += ["", "Strengths to preserve:"]
    if summary.keep:
        for item in summary.keep:
            lines.append(f"- {item.name} ({item.score}/10): {'; '.join(item.positives) or 'strong'}")
    else:
        lines.append("- None scored 8 or above; keep what is listed under 'Working well'.")
    lines.append("</logo_analysis>")
    return "\n".join(lines)