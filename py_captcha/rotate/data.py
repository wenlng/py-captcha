"""
Data models for rotate captcha results.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

from py_captcha.base import imagedata
from py_captcha.rotate.block import Block


class CaptchaData:
    """Interface for rotate captcha result data."""

    def get_data(self) -> Block:
        """Return block data."""
        raise NotImplementedError

    def get_master_image(self) -> imagedata.PNGImageData:
        """Return the main image."""
        raise NotImplementedError

    def get_thumb_image(self) -> imagedata.PNGImageData:
        """Return the thumbnail image."""
        raise NotImplementedError


class CaptData(CaptchaData):
    """Concrete rotate captcha result container."""

    def __init__(self, block: Block, master_image: imagedata.PNGImageData, thumb_image: imagedata.PNGImageData):
        self._block = block
        self._master_image = master_image
        self._thumb_image = thumb_image

    def get_data(self) -> Block:
        """Return block data."""
        return self._block

    def get_master_image(self) -> imagedata.PNGImageData:
        """Return the main image."""
        return self._master_image

    def get_thumb_image(self) -> imagedata.PNGImageData:
        """Return the thumbnail image."""
        return self._thumb_image
