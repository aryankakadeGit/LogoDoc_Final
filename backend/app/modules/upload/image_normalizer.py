"""
Decodes raster images with Pillow, checks corruption/dimensions, strips metadata, re-encodes for the AI.
"""
"""
Decodes a raster image and re-encodes it as a clean PNG:
- fully decodes the image (catches corrupted/truncated files)
- rejects decompression bombs before decoding
- applies EXIF rotation, then drops all metadata (EXIF/GPS) by re-encoding
- keeps transparency only when the image has it
- shrinks (never enlarges) to fit max_dimension
- animated images: first frame only
"""

import io

from PIL import Image, ImageOps, UnidentifiedImageError

from app.modules.upload.errors import ImageTooLarge, InvalidImage

MAX_PIXELS = 40_000_000  # ~6300 x 6300; guards memory before decoding

_PILLOW_FORMATS = {"png": "PNG", "jpeg": "JPEG", "webp": "WEBP"}


def normalize_image(data: bytes, fmt: str, max_dimension: int) -> tuple[bytes, int, int]:
    try:
        with Image.open(io.BytesIO(data), formats=[_PILLOW_FORMATS[fmt]]) as img:
            if img.width * img.height > MAX_PIXELS:
                raise ImageTooLarge()
            img.load()
            img = ImageOps.exif_transpose(img)
            img = img.convert("RGBA" if img.has_transparency_data else "RGB")
    except Image.DecompressionBombError as exc:
        raise ImageTooLarge() from exc
    except (UnidentifiedImageError, OSError, ValueError, SyntaxError) as exc:
        raise InvalidImage() from exc

    img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
    out = io.BytesIO()
    img.save(out, format="PNG")
    return out.getvalue(), img.width, img.height