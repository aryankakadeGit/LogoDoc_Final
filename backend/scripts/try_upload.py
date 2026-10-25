"""
Manual check for the upload module.

Usage (from backend/):
    python -m scripts.try_upload path/to/logo.svg [max_mb] [max_dimension]

Prints the result and saves the prepared PNG next to the input as <file>.prepared.png
"""

import sys
from pathlib import Path

from app.core.exceptions import AppError
from app.modules.upload import prepare_image


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1])
    max_mb = float(sys.argv[2]) if len(sys.argv) > 2 else 5
    max_dimension = int(sys.argv[3]) if len(sys.argv) > 3 else 2048

    try:
        result = prepare_image(
            path.read_bytes(), max_bytes=int(max_mb * 1024 * 1024), max_dimension=max_dimension
        )
    except AppError as err:
        sys.exit(f"REJECTED  {err.status_code} {err.code}: {err.message}")

    out = path.with_name(f"{path.name}.prepared.png")
    out.write_bytes(result.png_bytes)
    print(f"OK  {result!r}\n    saved -> {out} ({len(result.png_bytes):,} bytes)")


if __name__ == "__main__":
    main()