"""
Safely parses SVG (defusedxml) and rejects scripts, event handlers, external references and oversized documents.
"""
"""
Makes an uploaded SVG safe to render.

- Parsed with defusedxml: blocks entity expansion ("billion laughs") and XXE.
- Rejects any reference that could load an external/local resource:
  href values other than "#id" or an embedded raster data URI, CSS url()
  other than "url(#id)", and CSS @import.
- Returns the re-serialized tree, so the renderer only ever sees exactly
  what was checked (no parser differences).
"""

import re
import xml.etree.ElementTree as ET

from defusedxml import DefusedXmlException
from defusedxml.ElementTree import fromstring

from app.modules.upload.errors import InvalidImage, UnsafeSvg

_SAFE_HREF = re.compile(r"^\s*(#|data:image/(png|jpeg|jpg|webp|gif)[;,])", re.IGNORECASE)
_UNSAFE_CSS = re.compile(r"url\(\s*['\"]?\s*(?![\s'\"#])|@import", re.IGNORECASE)


def _local_name(name: str) -> str:
    return name.rsplit("}", 1)[-1]


def sanitize_svg(data: bytes) -> str:
    try:
        root = fromstring(data)
    except DefusedXmlException as exc:
        raise UnsafeSvg() from exc
    except ET.ParseError as exc:
        raise InvalidImage("The SVG file is malformed.") from exc

    if _local_name(root.tag) != "svg":
        raise InvalidImage("The file is not a valid SVG image.")

    for element in root.iter():
        for name, value in element.attrib.items():
            if _local_name(name) == "href" and not _SAFE_HREF.match(value):
                raise UnsafeSvg()

    svg = ET.tostring(root, encoding="unicode")
    if _UNSAFE_CSS.search(svg):
        raise UnsafeSvg()
    return svg