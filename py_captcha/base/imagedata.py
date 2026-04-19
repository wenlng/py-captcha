"""
Image wrapper helpers for exporting generated captcha images.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

import base64
import io

from PIL import Image


class JPEGImageData:
    """Wrapper around a generated image that is exported as JPEG."""

    def __init__(self, image: Image.Image):
        self._image = image

    def get(self) -> Image.Image:
        """Return the underlying PIL image object."""
        return self._image

    def to_bytes(self, quality: int = 100) -> bytes:
        """Serialize the image to JPEG bytes."""
        output = io.BytesIO()
        self._image.convert("RGB").save(output, format="JPEG", quality=quality)
        return output.getvalue()

    def to_base64(self, quality: int = 100) -> str:
        """Serialize the image to a data-URI base64 JPEG string."""
        data = self.to_bytes(quality)
        b64_data = base64.b64encode(data).decode("utf-8")
        return f"data:image/jpeg;base64,{b64_data}"

    def to_base64_data(self, quality: int = 100) -> str:
        """Serialize the image to a raw base64 JPEG payload."""
        data = self.to_bytes(quality)
        return base64.b64encode(data).decode("utf-8")

    def save_to_file(self, filepath: str, quality: int = 100) -> None:
        """Save the wrapped image to a JPEG file."""
        self._image.convert("RGB").save(filepath, format="JPEG", quality=quality)


class PNGImageData:
    """Wrapper around a generated image that is exported as PNG."""

    def __init__(self, image: Image.Image):
        self._image = image

    def get(self) -> Image.Image:
        """Return the underlying PIL image object."""
        return self._image

    def to_bytes(self) -> bytes:
        """Serialize the image to PNG bytes."""
        output = io.BytesIO()
        self._image.save(output, format="PNG")
        return output.getvalue()

    def to_base64(self) -> str:
        """Serialize the image to a data-URI base64 PNG string."""
        data = self.to_bytes()
        b64_data = base64.b64encode(data).decode("utf-8")
        return f"data:image/png;base64,{b64_data}"

    def to_base64_data(self) -> str:
        """Serialize the image to a raw base64 PNG payload."""
        data = self.to_bytes()
        return base64.b64encode(data).decode("utf-8")

    def save_to_file(self, filepath: str) -> None:
        """Save the wrapped image to a PNG file."""
        self._image.save(filepath, format="PNG")
