"""
Converts a sanitized SVG to PNG bytes offline, with output dimension limits.
"""
"""
Renders a sanitized SVG to PNG with resvg (no system libraries needed).
The output fits inside max_dimension x max_dimension, keeping aspect ratio.
"""

import resvg_py

from app.modules.upload.errors import InvalidImage


def rasterize_svg(svg: str, max_dimension: int) -> bytes:
    try:
        return resvg_py.svg_to_bytes(svg_string=svg, width=max_dimension, height=max_dimension)
    except ValueError as exc:
        raise InvalidImage("The SVG could not be rendered.") from exc