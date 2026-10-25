"""
Upload errors. Messages are safe to show to the user.
"""

from app.core.exceptions import AppError


class EmptyFile(AppError):
    code = "EMPTY_FILE"
    status_code = 400
    message = "The uploaded file is empty."


class FileTooLarge(AppError):
    code = "FILE_TOO_LARGE"
    status_code = 413
    message = "The uploaded file is too large."


class UnsupportedFormat(AppError):
    code = "UNSUPPORTED_FORMAT"
    status_code = 415
    message = "Unsupported file type. Please upload a PNG, JPG, WebP or SVG image."


class InvalidImage(AppError):
    code = "INVALID_IMAGE"
    status_code = 422
    message = "The image could not be read. It may be corrupted."


class ImageTooLarge(AppError):
    code = "IMAGE_TOO_LARGE"
    status_code = 413
    message = "The image dimensions are too large."


class UnsafeSvg(AppError):
    code = "UNSAFE_SVG"
    status_code = 422
    message = "The SVG contains external references or unsafe content."