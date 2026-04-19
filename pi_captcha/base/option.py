"""
Option value types shared across captcha modules.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""


class RangeVal:
    """Inclusive minimum and maximum range values."""

    def __init__(self, min_val: int, max_val: int):
        self.min = min_val
        self.max = max_val


class Size:
    """Simple width and height container."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height


class Point:
    """Simple x and y coordinate container."""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


DISTORT_NONE = 0
DISTORT_LEVEL1 = 1
DISTORT_LEVEL2 = 2
DISTORT_LEVEL3 = 3
DISTORT_LEVEL4 = 4
DISTORT_LEVEL5 = 5

QUALITY_NONE = 100
QUALITY_LEVEL1 = 95
QUALITY_LEVEL2 = 85
QUALITY_LEVEL3 = 75
QUALITY_LEVEL4 = 65
QUALITY_LEVEL5 = 55
