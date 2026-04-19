"""
Resource containers for rotate captcha generation.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

from typing import List

from PIL import Image


class Resources:
    """Container for rotate captcha resource collections."""

    def __init__(self):
        self.rang_images: List[Image.Image] = []


def default_resource() -> Resources:
    """Return default rotate captcha resources."""
    return Resources()
