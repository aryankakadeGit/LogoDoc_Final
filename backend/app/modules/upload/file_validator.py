"""
Validates raw upload bytes: not empty, within size limit, and a supported format.
The format is detected from the file content (magic bytes), never from the
filename or Content-Type, so a renamed file cannot spoof its type.
"""

from app.modules.upload.errors import EmptyFile, FileTooLarge, UnsupportedFormat
from app.modules.upload.schemas import SourceFormat

_SVG_SNIFF_BYTES = 4096


def detect_format(data: bytes) -> SourceFormat:
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    head = data[:_SVG_SNIFF_BYTES].lstrip(b"\xef\xbb\xbf \t\r\n").lower()
    if head.startswith(b"<") and b"<svg" in head:
        return "svg"
    raise UnsupportedFormat()


def validate_file(data: bytes, max_bytes: int) -> SourceFormat:
    if not data:
        raise EmptyFile()
    if len(data) > max_bytes:
        raise FileTooLarge(f"The file exceeds the {max_bytes / (1024 * 1024):g} MB limit.")
    return detect_format(data)