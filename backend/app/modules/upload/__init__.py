"""
Public API of the upload module. Other modules import only from here.
"""

from app.modules.upload.errors import (
    EmptyFile,
    FileTooLarge,
    ImageTooLarge,
    InvalidImage,
    UnsafeSvg,
    UnsupportedFormat,
)
from app.modules.upload.schemas import PreparedImage
from app.modules.upload.service import prepare_image

__all__ = [
    "prepare_image",
    "PreparedImage",
    "EmptyFile",
    "FileTooLarge",
    "ImageTooLarge",
    "InvalidImage",
    "UnsafeSvg",
    "UnsupportedFormat",
]