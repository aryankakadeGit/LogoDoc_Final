"""
Score maths. The backend is the final authority: the AI never supplies the overall score.
Rounding is "half up" (8.25 -> 8.3), which is what users expect; Python's round() would give 8.2.
"""

from collections.abc import Iterable
from decimal import ROUND_HALF_UP, Decimal


def round_score(value: float) -> float:
    return float(Decimal(str(value)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def overall_score(scores: Iterable[float | None]) -> float:
    """Average of the applicable (non-None) scores, using the same rounded values the user sees."""
    applicable = [Decimal(str(round_score(s))) for s in scores if s is not None]
    if not applicable:
        raise ValueError("no applicable scores")
    return round_score(float(sum(applicable) / len(applicable)))