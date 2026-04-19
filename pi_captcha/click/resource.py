"""
Resource containers for click captcha generation.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

from typing import Dict, List

from PIL import Image


class Resources:
    """Container for click captcha resource collections."""

    def __init__(self):
        self.chars: List[str] = []
        self.shape_maps: Dict[str, Image.Image] = {}
        self.shapes: List[str] = []
        self.rang_fonts: List = []
        self.rang_backgrounds: List[Image.Image] = []
        self.rang_thumb_backgrounds: List[Image.Image] = []


def default_resource() -> Resources:
    """Return default click captcha resources."""
    resources = Resources()
    resources.chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
    return resources
