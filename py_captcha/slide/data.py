"""
Data models for slide captcha results.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

from py_captcha.base import imagedata
from py_captcha.slide.block import Block


class CaptchaData:
    """Interface for slide captcha result data."""

    def get_data(self) -> Block:
        """Return block data."""
        raise NotImplementedError

    def get_master_image(self) -> imagedata.JPEGImageData:
        """Return the main image."""
        raise NotImplementedError

    def get_tile_image(self) -> imagedata.PNGImageData:
        """Return the puzzle tile image."""
        raise NotImplementedError


class CaptData(CaptchaData):
    """Concrete slide captcha result container."""

    def __init__(self, block: Block, master_image: imagedata.JPEGImageData, tile_image: imagedata.PNGImageData):
        self._block = block
        self._master_image = master_image
        self._tile_image = tile_image

    def get_data(self) -> Block:
        """Return block data."""
        return self._block

    def get_master_image(self) -> imagedata.JPEGImageData:
        """Return the main image."""
        return self._master_image

    def get_tile_image(self) -> imagedata.PNGImageData:
        """Return the puzzle tile image."""
        return self._tile_image
