"""
Options for click captcha generation.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

from typing import List, Optional

from py_captcha.base import option


class Options:
    """Configuration values for click captcha generation."""

    def __init__(self):
        self.font_dpi = 72
        self.image_size: Optional[option.Size] = None
        self.range_len: Optional[option.RangeVal] = None
        self.range_angle_pos: List[option.RangeVal] = []
        self.range_size: Optional[option.RangeVal] = None
        self.range_colors: List[str] = []
        self.display_shadow = True
        self.shadow_color = "#101010"
        self.shadow_point: Optional[option.Point] = None
        self.image_alpha = 1.0
        self.thumb_image_size: Optional[option.Size] = None
        self.range_verify_len: Optional[option.RangeVal] = None
        self.disabled_range_verify_len = False
        self.range_thumb_size: Optional[option.RangeVal] = None
        self.range_thumb_colors: List[str] = []
        self.range_thumb_bg_colors: List[str] = []
        self.thumb_bg_distort = option.DISTORT_LEVEL4
        self.thumb_bg_circles_num = 24
        self.thumb_bg_slim_line_num = 2
        self.is_thumb_non_deform_ability = True
        self.thumb_disturb_alpha = 1.0
        self.use_shape_original_color = False


def default_options() -> Options:
    """Return the default click captcha options."""
    opts = Options()
    colors = ["#fde98e", "#60c1ff", "#fcb08e", "#fb88ff", "#b4fed4", "#cbfaa9", "#78d6f8"]
    thumb_colors = ["#1f55c4", "#780592", "#2f6b00", "#910000", "#864401", "#675901", "#016e5c"]
    opts.range_len = option.RangeVal(min_val=6, max_val=7)
    opts.range_angle_pos = [
        option.RangeVal(min_val=20, max_val=35),
        option.RangeVal(min_val=35, max_val=45),
        option.RangeVal(min_val=45, max_val=60),
        option.RangeVal(min_val=290, max_val=305),
        option.RangeVal(min_val=305, max_val=325),
        option.RangeVal(min_val=325, max_val=330),
    ]
    opts.range_size = option.RangeVal(min_val=26, max_val=32)
    opts.range_colors = colors
    opts.display_shadow = True
    opts.shadow_color = "#101010"
    opts.shadow_point = option.Point(x=-1, y=-1)
    opts.image_size = option.Size(width=300, height=220)
    opts.image_alpha = 1.0
    opts.range_verify_len = option.RangeVal(min_val=2, max_val=4)
    opts.disabled_range_verify_len = False
    opts.thumb_image_size = option.Size(width=150, height=40)
    opts.range_thumb_size = option.RangeVal(min_val=22, max_val=28)
    opts.range_thumb_colors = thumb_colors
    opts.range_thumb_bg_colors = thumb_colors
    opts.thumb_bg_distort = option.DISTORT_LEVEL4
    opts.thumb_bg_circles_num = 24
    opts.thumb_bg_slim_line_num = 2
    opts.is_thumb_non_deform_ability = True
    opts.thumb_disturb_alpha = 1.0
    return opts
