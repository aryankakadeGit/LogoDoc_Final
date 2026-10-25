"""
Shared pytest fixtures: test settings, fake AI provider, sample images, test client.
"""
"""
Shared pytest fixtures.
"""

import io

import pytest
from PIL import Image


@pytest.fixture
def make_image():
    """Build an in-memory image: make_image("PNG", (w, h), mode="RGBA", **save_kwargs) -> bytes."""

    def _make(fmt: str = "PNG", size=(64, 32), mode: str = "RGB", color="red", **save_kwargs) -> bytes:
        buf = io.BytesIO()
        Image.new(mode, size, color).save(buf, format=fmt, **save_kwargs)
        return buf.getvalue()

    return _make