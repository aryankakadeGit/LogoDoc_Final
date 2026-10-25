"""
Upload pipeline: validate -> (sanitize + rasterize if SVG) -> normalize -> return a safe image for analysis.
"""
"""
Upload pipeline: validate -> (sanitize + rasterize if SVG) -> normalize.
Everything happens in memory; nothing is written to disk.
"""

from app.modules.upload.file_validator import validate_file
from app.modules.upload.image_normalizer import normalize_image
from app.modules.upload.schemas import PreparedImage
from app.modules.upload.svg_rasterizer import rasterize_svg
from app.modules.upload.svg_sanitizer import sanitize_svg


def prepare_image(data: bytes, *, max_bytes: int, max_dimension: int) -> PreparedImage:
    source_format = validate_file(data, max_bytes)

    raster, raster_format = data, source_format
    if source_format == "svg":
        raster, raster_format = rasterize_svg(sanitize_svg(data), max_dimension), "png"

    png_bytes, width, height = normalize_image(raster, raster_format, max_dimension)
    return PreparedImage(
        png_bytes=png_bytes, width=width, height=height, source_format=source_format
    )