"""
Tests for upload.svg_rasterizer
"""
import io

import pytest
from PIL import Image

from app.modules.upload.errors import InvalidImage
from app.modules.upload.svg_rasterizer import rasterize_svg


def _size(png: bytes) -> tuple[int, int]:
    return Image.open(io.BytesIO(png)).size


@pytest.mark.parametrize(
    "viewbox, expected",
    [("0 0 200 100", (512, 256)), ("0 0 100 400", (128, 512)), ("0 0 10 10", (512, 512))],
)
def test_fits_inside_max_dimension_keeping_aspect(viewbox, expected):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}">'
        '<rect width="100%" height="100%"/></svg>'
    )
    assert _size(rasterize_svg(svg, 512)) == expected


def test_huge_declared_size_is_capped():
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="100000" height="100000">'
        '<rect width="5" height="5"/></svg>'
    )
    assert _size(rasterize_svg(svg, 512)) == (512, 512)


def test_unrenderable_svg_raises_invalid_image():
    with pytest.raises(InvalidImage):
        rasterize_svg("not svg at all", 512)