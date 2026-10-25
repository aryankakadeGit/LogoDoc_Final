"""
Tests for upload.image_normalizer
"""
import io

import pytest
from PIL import Image

from app.modules.upload import image_normalizer
from app.modules.upload.errors import ImageTooLarge, InvalidImage
from app.modules.upload.image_normalizer import normalize_image


def _open(png: bytes) -> Image.Image:
    img = Image.open(io.BytesIO(png))
    assert img.format == "PNG"
    return img


def test_large_image_is_shrunk_keeping_aspect(make_image):
    png, w, h = normalize_image(make_image("PNG", (4000, 2000)), "png", 2048)
    assert (w, h) == (2048, 1024) == _open(png).size


def test_small_image_is_not_enlarged(make_image):
    _, w, h = normalize_image(make_image("PNG", (64, 32)), "png", 2048)
    assert (w, h) == (64, 32)


def test_transparency_is_kept(make_image):
    png, *_ = normalize_image(make_image("PNG", mode="RGBA", color=(0, 0, 0, 0)), "png", 2048)
    assert _open(png).mode == "RGBA"


def test_opaque_image_has_no_alpha(make_image):
    png, *_ = normalize_image(make_image("JPEG"), "jpeg", 2048)
    assert _open(png).mode == "RGB"


@pytest.mark.parametrize("mode", ["L", "P", "CMYK", "I;16", "LA"])
def test_unusual_modes_are_converted(make_image, mode):
    fmt = "JPEG" if mode == "CMYK" else "PNG"
    color = 0 if mode in ("L", "P", "I;16") else None
    png, *_ = normalize_image(make_image(fmt, mode=mode, color=color), fmt.lower(), 2048)
    assert _open(png).mode in ("RGB", "RGBA")


def test_exif_rotation_applied_and_metadata_removed():
    exif = Image.Exif()
    exif[0x0112] = 6  # Orientation: rotate 90° clockwise
    exif[0x010F] = "SecretCameraMaker"
    buf = io.BytesIO()
    Image.new("RGB", (60, 20), "blue").save(buf, "JPEG", exif=exif)

    png, w, h = normalize_image(buf.getvalue(), "jpeg", 2048)
    assert (w, h) == (20, 60)
    assert b"SecretCameraMaker" not in png
    assert not _open(png).getexif()


def test_animated_webp_uses_first_frame():
    frames = [Image.new("RGB", (16, 16), c) for c in ("red", "blue")]
    buf = io.BytesIO()
    frames[0].save(buf, "WEBP", save_all=True, append_images=frames[1:], lossless=True)
    png, *_ = normalize_image(buf.getvalue(), "webp", 2048)
    assert _open(png).convert("RGB").getpixel((8, 8)) == (255, 0, 0)


def test_truncated_image_rejected(make_image):
    data = make_image("PNG", (300, 300))
    with pytest.raises(InvalidImage):
        normalize_image(data[: len(data) // 2], "png", 2048)


def test_garbage_with_valid_magic_rejected():
    with pytest.raises(InvalidImage):
        normalize_image(b"\x89PNG\r\n\x1a\n" + b"garbage" * 50, "png", 2048)


def test_format_mismatch_rejected(make_image):
    with pytest.raises(InvalidImage):
        normalize_image(make_image("JPEG"), "png", 2048)


def test_pixel_limit_rejected_before_decoding(make_image, monkeypatch):
    monkeypatch.setattr(image_normalizer, "MAX_PIXELS", 100)
    with pytest.raises(ImageTooLarge):
        normalize_image(make_image("PNG", (20, 20)), "png", 2048)