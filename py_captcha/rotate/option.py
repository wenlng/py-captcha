"""
Options for rotate captcha generation.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

from typing import List

from py_captcha.base import option


class Options:
    """Configuration values for rotate captcha generation."""

    def __init__(self):
        self.image_square_size = 220
        self.range_angle_pos: List[option.RangeVal] = []
        self.range_thumb_image_square_size: List[int] = []
        self.thumb_image_alpha = 1.0


def default_options() -> Options:
    """Return the default rotate captcha options."""
    opts = Options()
    opts.image_square_size = 220
    opts.range_angle_pos = [option.RangeVal(min_val=0, max_val=360)]
    opts.range_thumb_image_square_size = [120]
    opts.thumb_image_alpha = 1.0
    return opts
