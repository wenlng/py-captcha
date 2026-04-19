"""
Shared helper functions for image and color processing.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

import math
import os
import re
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFilter

from py_captcha.base import random as base_random


def format_alpha(val: float) -> int:
    """Convert an alpha ratio in the range 0-1 into an 8-bit integer."""
    a = min(val, 1.0)
    alpha = a * 255
    return int(alpha)


def rgb_to_hex(red: int, green: int, blue: int) -> str:
    """Convert an RGB color tuple into a hex string without the leading hash."""

    def t2x(t: int) -> str:
        result = hex(t)[2:]
        if len(result) == 1:
            result = "0" + result
        return result

    r = t2x(red)
    g = t2x(green)
    b = t2x(blue)
    return r + g + b


def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    """Convert a hex color string into an RGB tuple."""
    hex_str = hex_str.lstrip("#")
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return r, g, b


def parse_hex_color(s: str) -> Tuple[int, int, int, int]:
    """Parse a hex color string into an RGBA tuple."""
    if not s.startswith("#"):
        raise ValueError("hex color must start with '#'")

    s = s[1:]
    if len(s) == 6:
        r = int(s[0:2], 16)
        g = int(s[2:4], 16)
        b = int(s[4:6], 16)
        return r, g, b, 255
    if len(s) == 3:
        r = int(s[0], 16) * 17
        g = int(s[1], 16) * 17
        b = int(s[2], 16) * 17
        return r, g, b, 255
    raise ValueError("hex color format invalid")


def path_exists(path: str) -> bool:
    """Return whether a filesystem path exists."""
    return os.path.exists(path)


def in_array_with_str(items: list, s: str) -> bool:
    """Return whether a string exists in a list."""
    return s in items


def is_chinese_char(s: str) -> bool:
    """Return whether the input contains any CJK Unified Ideographs."""
    return bool(re.search(r"[\u4e00-\u9fff]", s))


def len_chinese_char(s: str) -> int:
    """Return the visual character count for a string."""
    return len(s)


def rand_index(length: int) -> int:
    """Generate a random index using a thread-local random generator."""
    if length <= 0:
        return -1

    from py_captcha.base.thread_random import get_thread_random

    rng = get_thread_random()
    return rng.randint(0, length - 1)


def random_crop_resize(image: Optional[Image.Image], target_width: int, target_height: int) -> Image.Image:
    """Randomly crop and resize an image while preserving aspect ratio."""
    if target_width <= 0 or target_height <= 0:
        raise ValueError("target size must be positive")

    if image is None:
        return Image.new("RGBA", (target_width, target_height), (255, 255, 255, 255))

    image = image.convert("RGBA")
    source_width, source_height = image.size
    if source_width <= 0 or source_height <= 0:
        return Image.new("RGBA", (target_width, target_height), (255, 255, 255, 255))

    target_ratio = target_width / target_height
    source_ratio = source_width / source_height

    if math.isclose(source_ratio, target_ratio, rel_tol=1e-9, abs_tol=1e-9):
        crop_left = 0
        crop_top = 0
        crop_width = source_width
        crop_height = source_height
    elif source_ratio > target_ratio:
        crop_height = source_height
        crop_width = max(1, int(round(crop_height * target_ratio)))
        max_left = max(source_width - crop_width, 0)
        crop_left = base_random.rand_int(0, max_left) if max_left > 0 else 0
        crop_top = 0
    else:
        crop_width = source_width
        crop_height = max(1, int(round(crop_width / target_ratio)))
        max_top = max(source_height - crop_height, 0)
        crop_left = 0
        crop_top = base_random.rand_int(0, max_top) if max_top > 0 else 0

    cropped = image.crop((
        crop_left,
        crop_top,
        crop_left + crop_width,
        crop_top + crop_height,
    ))
    return cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)


def high_quality_rotate(image: Image.Image, angle: float, scale: int = 4) -> Image.Image:
    """Rotate an image with supersampling to reduce aliasing artifacts."""
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    normalized_angle = angle % 360
    if normalized_angle == 0:
        return image.copy()

    scale = max(int(scale), 1)
    if scale == 1:
        return image.rotate(-normalized_angle, expand=True, resample=Image.Resampling.BICUBIC, fillcolor=(0, 0, 0, 0))

    upscaled = image.resize(
        (max(1, image.width * scale), max(1, image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    rotated = upscaled.rotate(
        -normalized_angle,
        expand=True,
        resample=Image.Resampling.BICUBIC,
        fillcolor=(0, 0, 0, 0),
    )
    return rotated.resize(
        (max(1, round(rotated.width / scale)), max(1, round(rotated.height / scale))),
        Image.Resampling.LANCZOS,
    )


def create_anti_aliased_ellipse_mask(width: int, height: int, scale: int = 4, blur_radius: float = 0.35) -> Image.Image:
    """Create an anti-aliased elliptical mask image."""
    width = max(int(width), 1)
    height = max(int(height), 1)
    scale = max(int(scale), 1)

    mask = Image.new("L", (width * scale, height * scale), 0)
    draw = ImageDraw.Draw(mask)
    inset = max(scale // 2, 1)
    draw.ellipse((inset, inset, width * scale - inset - 1, height * scale - inset - 1), fill=255)

    if blur_radius > 0:
        mask = mask.filter(ImageFilter.GaussianBlur(radius=blur_radius * scale))

    return mask.resize((width, height), Image.Resampling.LANCZOS)
