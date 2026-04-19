"""
Options for slide captcha generation.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

from typing import List, Optional

from py_captcha.base import option


class DeadZoneDirectionType:
    """Dead-zone direction constants."""

    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3


class Options:
    """Configuration values for slide captcha generation."""

    def __init__(self):
        self.image_size: Optional[option.Size] = None
        self.image_alpha = 1.0
        self.range_dead_zone_directions: List[int] = []
        self.range_graph_size: Optional[option.RangeVal] = None
        self.range_graph_angle_pos: List[option.RangeVal] = []
        self.gen_graph_number = 1
        self.enable_graph_vertical_random = False


def default_options() -> Options:
    """Return the default slide captcha options."""
    opts = Options()
    opts.image_size = option.Size(width=300, height=220)
    opts.image_alpha = 1.0
    opts.range_dead_zone_directions = [DeadZoneDirectionType.LEFT]
    opts.range_graph_size = option.RangeVal(min_val=50, max_val=60)
    opts.range_graph_angle_pos = [
        option.RangeVal(min_val=0, max_val=0),
        option.RangeVal(min_val=0, max_val=0),
    ]
    opts.gen_graph_number = 1
    opts.enable_graph_vertical_random = False
    return opts
