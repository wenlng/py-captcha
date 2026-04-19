"""
Data models for click captcha results.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

from typing import Dict

from py_captcha.base import imagedata
from py_captcha.click.dot import Dot


class CaptchaData:
    """Interface for click captcha result data."""

    def get_data(self) -> Dict[int, Dot]:
        """Return dot data."""
        raise NotImplementedError

    def get_master_image(self) -> imagedata.JPEGImageData:
        """Return the main image."""
        raise NotImplementedError

    def get_thumb_image(self) -> imagedata.PNGImageData:
        """Return the thumbnail image."""
        raise NotImplementedError


class CaptData(CaptchaData):
    """Concrete click captcha result container."""

    def __init__(self, dots: Dict[int, Dot], master_image: imagedata.JPEGImageData, thumb_image: imagedata.PNGImageData):
        self._dots = dots
        self._master_image = master_image
        self._thumb_image = thumb_image

    def get_data(self) -> Dict[int, Dot]:
        """Return dot data."""
        return self._dots

    def get_master_image(self) -> imagedata.JPEGImageData:
        """Return the main image."""
        return self._master_image

    def get_thumb_image(self) -> imagedata.PNGImageData:
        """Return the thumbnail image."""
        return self._thumb_image
