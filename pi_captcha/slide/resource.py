"""
Resource containers for slide captcha generation.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

from typing import List

from PIL import Image

from pi_captcha.slide.block import GraphImage


class Resources:
    """Container for slide captcha resource collections."""

    def __init__(self):
        self.rang_backgrounds: List[Image.Image] = []
        self.rang_graph_image: List[GraphImage] = []


def default_resource() -> Resources:
    """Return default slide captcha resources."""
    return Resources()
