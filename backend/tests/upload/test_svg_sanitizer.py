"""
Tests for upload.svg_sanitizer
"""
import pytest

from app.modules.upload.errors import InvalidImage, UnsafeSvg
from app.modules.upload.svg_sanitizer import sanitize_svg

NS = 'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"'


def svg(body: str) -> bytes:
    return f'<svg {NS} viewBox="0 0 10 10">{body}</svg>'.encode()


def test_plain_svg_passes():
    out = sanitize_svg(svg('<rect width="10" height="10" fill="red"/>'))
    assert "rect" in out


def test_standard_doctype_is_allowed():
    data = (
        b'<?xml version="1.0"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" '
        b'"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">' + svg("<rect/>")
    )
    assert "rect" in sanitize_svg(data)


@pytest.mark.parametrize(
    "body",
    [
        '<use href="#a"/>',
        '<use xlink:href="#a"/>',
        '<image href="data:image/png;base64,iVBORw0KGgo="/>',
        '<rect style="fill:url(#grad)"/>',
        "<style>.a{fill:url( '#g' )}</style>",
    ],
)
def test_internal_refs_and_embedded_rasters_allowed(body):
    sanitize_svg(svg(body))


@pytest.mark.parametrize(
    "body",
    [
        '<image href="https://evil.example/x.png"/>',
        '<image xlink:href="file:///etc/passwd"/>',
        '<image href="logo.png"/>',
        '<image href="data:image/svg+xml;base64,PHN2Zy8+"/>',
        '<rect style="fill:url(https://evil.example/p)"/>',
        "<style>@import 'https://evil.example/a.css';</style>",
        '<rect fill="url(other.svg#g)"/>',
    ],
)
def test_external_refs_rejected(body):
    with pytest.raises(UnsafeSvg):
        sanitize_svg(svg(body))


def test_entity_expansion_rejected():
    bomb = (
        b'<?xml version="1.0"?><!DOCTYPE svg [<!ENTITY a "aaaaaaaaaa">'
        b'<!ENTITY b "&a;&a;&a;&a;&a;&a;&a;&a;&a;&a;">]>'
        b'<svg xmlns="http://www.w3.org/2000/svg"><text>&b;</text></svg>'
    )
    with pytest.raises(UnsafeSvg):
        sanitize_svg(bomb)


def test_external_entity_rejected():
    xxe = (
        b'<?xml version="1.0"?><!DOCTYPE svg [<!ENTITY x SYSTEM "file:///etc/passwd">]>'
        b'<svg xmlns="http://www.w3.org/2000/svg"><text>&x;</text></svg>'
    )
    with pytest.raises(UnsafeSvg):
        sanitize_svg(xxe)


def test_malformed_xml_rejected():
    with pytest.raises(InvalidImage):
        sanitize_svg(b"<svg><rect></svg>")


def test_non_svg_root_rejected():
    with pytest.raises(InvalidImage):
        sanitize_svg(b"<html><svg/></html>")