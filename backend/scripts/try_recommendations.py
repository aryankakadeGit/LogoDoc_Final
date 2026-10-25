"""
Manual check for recommendations against the REAL AI, using an analysis saved by try_analysis.
Uses 2 text-only AI calls (one per type); the image is not analysed again.

Usage (from backend/):
    python -m scripts.try_recommendations path/to/logo.png.analysis.json

Prints the improved prompt and the designer recommendations, and saves the .txt download
next to the JSON as <file>.designer.txt
"""

import asyncio
import sys
from pathlib import Path

from app.core.config import get_settings
from app.core.exceptions import AppError
from app.core.logging import setup_logging
from app.modules.ai import create_provider
from app.modules.analysis import LogoAnalysis
from app.modules.recommendations.ai_generated import generate_improved_prompt
from app.modules.recommendations.manual_design import build_txt, generate_designer_recommendations


async def run(path: Path) -> None:
    analysis = LogoAnalysis.model_validate_json(path.read_text(encoding="utf-8"))
    ai = create_provider(get_settings())

    improved = await generate_improved_prompt(analysis, ai)
    print("=== AI GENERATED: improved prompt ===\n")
    print(improved.prompt)

    recs = await generate_designer_recommendations(analysis, ai)
    print("\n=== MANUALLY DESIGNED: designer recommendations ===")
    for r in recs.recommendations:
        print(f"\n{r.name} ({r.score}/10)")
        print(f"  What is wrong : {r.problem}")
        print(f"  Why it matters: {r.why_it_matters}")
        print(f"  What to change: {r.suggestion}")
        print(f"  What to keep  : {r.preserve}")
    print("\nOverall:")
    for i, text in enumerate(recs.overall, 1):
        print(f"  {i}. {text}")

    out = path.with_name(f"{path.name}.designer.txt")
    out.write_text(build_txt(analysis, recs), encoding="utf-8")
    print(f"\nTXT saved -> {out}")


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    setup_logging(get_settings().log_level)
    try:
        asyncio.run(run(Path(sys.argv[1])))
    except AppError as err:
        sys.exit(f"FAILED  {err.status_code} {err.code}: {err.message}")


if __name__ == "__main__":
    main()