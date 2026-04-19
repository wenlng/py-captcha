"""
Thread-safe random resource selectors.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

from typing import List, Optional

from PIL import Image

from py_captcha.base.thread_random import get_thread_random


def rand_string(items: List[str]) -> str:
    """Return a random string from the provided list."""
    if not items:
        return ""
    rng = get_thread_random()
    return rng.choice(items)


def rand_hex_color(colors: List[str]) -> str:
    """Return a random hex color from the provided list."""
    if not colors:
        return "#000000"
    rng = get_thread_random()
    return rng.choice(colors)


def rand_font(fonts: List) -> Optional:
    """Return a random font object from the provided list."""
    if not fonts:
        return None
    rng = get_thread_random()
    return rng.choice(fonts)


def rand_image(images: List[Image.Image]) -> Optional[Image.Image]:
    """Return a random image from the provided list."""
    if not images:
        return None
    rng = get_thread_random()
    return rng.choice(images)
