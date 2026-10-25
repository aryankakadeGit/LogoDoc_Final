"""
Manual check for the ai module against the REAL Gemini API (uses your backend/.env).

Usage (from backend/):
    python -m scripts.try_ai                      # list Flash models your key can use (no quota used)
    python -m scripts.try_ai path/to/logo.png     # 1 real AI call with the image (needs GEMINI_MODEL)
"""

import asyncio
import sys
from pathlib import Path

from google import genai
from google.genai import errors
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.exceptions import AppError
from app.core.logging import setup_logging
from app.modules.ai import create_provider
from app.modules.upload import prepare_image


class QuickCheck(BaseModel):
    is_logo: bool
    description: str


def list_models(api_key: str) -> None:
    client = genai.Client(api_key=api_key)
    print("Flash models available to your key:")
    for model in client.models.list():
        if "flash" in model.name:
            print("  ", model.name.removeprefix("models/"))


async def analyze(path: Path) -> None:
    settings = get_settings()
    image = prepare_image(
        path.read_bytes(),
        max_bytes=settings.max_upload_bytes,
        max_dimension=settings.max_image_dimension,
    )
    provider = create_provider(settings)
    text = await provider.generate_json(
        "Is this image a logo? Answer is_logo and describe it in one sentence.", QuickCheck, image.png_bytes
    )
    print("Raw AI JSON:", text)
    print("Validated  :", QuickCheck.model_validate_json(text))


def main() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)
    api_key = settings.gemini_api_key.get_secret_value()
    if not api_key:
        sys.exit("GEMINI_API_KEY is empty in backend/.env")

    try:
        if len(sys.argv) < 2:
            list_models(api_key)
        else:
            asyncio.run(analyze(Path(sys.argv[1])))
    except AppError as err:
        sys.exit(f"FAILED  {err.status_code} {err.code}: {err.message}")
    except errors.APIError as err:
        sys.exit(f"FAILED  {err.code} {err.status}: {err.message}")


if __name__ == "__main__":
    main()