"""
Tests for upload.service
"""
import io

import pytest
from PIL import Image
from pydantic import ValidationError

from app.modules.upload import (
    EmptyFile,
    FileTooLarge,
    PreparedImage,
    UnsafeSvg,
    UnsupportedFormat,
    prepare_image,
)

LIMITS = {"max_bytes": 5 * 1024 * 1024, "max_dimension": 2048}

SVG = (
    b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100">'
    b'<rect width="200" height="100" fill="red"/></svg>'
)


@pytest.mark.parametrize("fmt, expected", [("PNG", "png"), ("JPEG", "jpeg"), ("WEBP", "webp")])
def test_raster_formats_become_png(make_image, fmt, expected):
    result = prepare_image(make_image(fmt, (64, 32)), **LIMITS)
    assert isinstance(result, PreparedImage)
    assert result.source_format == expected
    assert (result.width, result.height) == (64, 32)
    assert Image.open(io.BytesIO(result.png_bytes)).format == "PNG"


def test_svg_is_rasterized_to_max_dimension():
    result = prepare_image(SVG, **LIMITS)
    assert result.source_format == "svg"
    assert (result.width, result.height) == (2048, 1024)
    assert Image.open(io.BytesIO(result.png_bytes)).size == (2048, 1024)


def test_spoofed_extension_does_not_matter(make_image):
    # Content decides the type, not the filename: a GIF is rejected whatever it's called.
    with pytest.raises(UnsupportedFormat):
        prepare_image(make_image("GIF"), **LIMITS)


def test_size_limit_checked_first():
    with pytest.raises(FileTooLarge):
        prepare_image(b"x" * 11, max_bytes=10, max_dimension=2048)


def test_empty_rejected():
    with pytest.raises(EmptyFile):
        prepare_image(b"", **LIMITS)


def test_unsafe_svg_rejected():
    bad = b'<svg xmlns="http://www.w3.org/2000/svg"><image href="https://evil.example/x.png"/></svg>'
    with pytest.raises(UnsafeSvg):
        prepare_image(bad, **LIMITS)


def test_result_is_immutable_and_hides_bytes_in_repr(make_image):
    result = prepare_image(make_image("PNG"), **LIMITS)
    assert "png_bytes" not in repr(result)
    with pytest.raises(ValidationError):
        result.width = 1