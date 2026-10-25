"""
Manual end-to-end check: upload -> real AI analysis -> validated, scored result. Uses 1 AI call
(2 if the first answer is invalid).

Usage (from backend/):
    python -m scripts.try_analysis path/to/logo.png

Prints a readable report and saves the full JSON next to the input as <file>.analysis.json
"""

import asyncio
import sys
from pathlib import Path

from app.core.config import get_settings
from app.core.exceptions import AppError
from app.core.logging import setup_logging
from app.modules.ai import create_provider
from app.modules.analysis import LogoAnalysis, analyze_logo
from app.modules.upload import prepare_image


async def run(path: Path) -> None:
    settings = get_settings()
    image = prepare_image(
        path.read_bytes(),
        max_bytes=settings.max_upload_bytes,
        max_dimension=settings.max_image_dimension,
    )
    result = await analyze_logo(image, create_provider(settings))

    out = path.with_name(f"{path.name}.analysis.json")
    out.write_text(result.model_dump_json(indent=2), encoding="utf-8")

    if not isinstance(result, LogoAnalysis):
        print(f"NOT A LOGO: {result.message}")
        return
    print(f"OVERALL SCORE: {result.overall_score}/10\n")
    for p in result.parameters:
        score = "N/A" if p.score is None else f"{p.score}/10"
        print(f"{p.name}: {score}")
        for text in p.positives:
            print(f"   + {text}")
        for text in p.negatives:
            print(f"   - {text}")
    s = result.similarity
    print(f"\nSimilarity: {s.match_level} (brand: {s.recognized_brand or '-'})")
    print(f"\nFull JSON saved -> {out}")


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