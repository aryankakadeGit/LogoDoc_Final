"""
Tests for upload.file_validator
"""
import pytest

from app.modules.upload.errors import EmptyFile, FileTooLarge, UnsupportedFormat
from app.modules.upload.file_validator import detect_format, validate_file

MB = 1024 * 1024


@pytest.mark.parametrize("fmt, expected", [("PNG", "png"), ("JPEG", "jpeg"), ("WEBP", "webp")])
def test_detects_raster_formats(make_image, fmt, expected):
    assert detect_format(make_image(fmt)) == expected


@pytest.mark.parametrize(
    "data",
    [
        b'<svg xmlns="http://www.w3.org/2000/svg"/>',
        b'\xef\xbb\xbf  <?xml version="1.0"?>\n<svg xmlns="http://www.w3.org/2000/svg"/>',
        b'<?xml version="1.0"?><!DOCTYPE svg><!-- c --><SVG/>',
    ],
)
def test_detects_svg(data):
    assert detect_format(data) == "svg"


@pytest.mark.parametrize(
    "data",
    [
        b"GIF89a....",
        b"%PDF-1.7",
        b"just some text",
        b"<html><body>hi</body></html>",
        b"RIFF\x00\x00\x00\x00WAVEfmt ",
    ],
)
def test_rejects_unsupported(data):
    with pytest.raises(UnsupportedFormat):
        detect_format(data)


def test_rejects_gif_image(make_image):
    with pytest.raises(UnsupportedFormat):
        detect_format(make_image("GIF"))


def test_empty_file():
    with pytest.raises(EmptyFile):
        validate_file(b"", 5 * MB)


def test_too_large_message_shows_limit():
    with pytest.raises(FileTooLarge, match="5 MB"):
        validate_file(b"\x89PNG\r\n\x1a\n" + b"0" * (5 * MB), 5 * MB)


def test_exactly_at_limit_is_allowed(make_image):
    data = make_image("PNG")
    assert validate_file(data, len(data)) == "png"