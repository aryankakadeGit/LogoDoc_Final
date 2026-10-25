"""
MVP checker: turns the similarity section of the existing AI analysis into a user-facing status.
No extra AI call. A brand name is only shown when the AI reports a strong or exact match.
"""

from app.modules.analysis import Similarity
from app.modules.logo_status.schemas import LogoStatus

SOURCE = "AI visual recognition of well-known logos"


def status_from_similarity(similarity: Similarity) -> LogoStatus:
    brand = (similarity.recognized_brand or "").strip() or None
    notes = similarity.notes
    sources = [SOURCE]

    if similarity.match_level == "exact_or_near_exact" and brand:
        return LogoStatus(
            status="matches_known_logo",
            title="Matches a known logo",
            message=f"This appears to be, or closely match, the {brand} logo.",
            recognized_brand=brand,
            notes=notes,
            sources_checked=sources,
        )
    if similarity.match_level in ("exact_or_near_exact", "strong_similarity"):
        target = f"the {brand} logo" if brand else "an existing well-known logo"
        return LogoStatus(
            status="potentially_similar",
            title="Potentially similar logo detected",
            message=f"Your logo looks visually similar to {target}. Consider reviewing it before use.",
            recognized_brand=brand,
            notes=notes,
            sources_checked=sources,
        )
    if similarity.match_level == "generic_elements":
        return LogoStatus(
            status="generic_elements",
            title="Uses common design elements",
            message=(
                "Your logo uses shapes or styles found in many logos. "
                "This is normal and does not mean it was copied."
            ),
            notes=notes,
            sources_checked=sources,
        )
    return LogoStatus(
        status="no_significant_similarity",
        title="No significant similarity detected",
        message="We did not find a close match with well-known logos.",
        notes=notes,
        sources_checked=sources,
    )