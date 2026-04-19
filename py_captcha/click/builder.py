"""
Builder utilities for click captcha generation.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

from typing import Callable, Dict, List

from PIL import Image

from py_captcha.base import option
from py_captcha.click.click import ClickCaptcha, Mode
from py_captcha.click.option import Options, default_options
from py_captcha.click.resource import Resources, default_resource


class ClickBuilder:
    """Builder for configuring and creating click captchas."""

    def __init__(self, *opts: Callable[[Options], None]):
        self._opts: List[Callable[[Options], None]] = list(opts)
        self._resources: List[Callable[[Resources], None]] = []

    def set_options(self, *opts: Callable[[Options], None]):
        """Append option mutators to the builder."""
        self._opts.extend(opts)
        return self

    def set_resources(self, *resources: Callable[[Resources], None]):
        """Append resource mutators to the builder."""
        self._resources.extend(resources)
        return self

    def clear(self):
        """Clear all accumulated options and resources."""
        self._opts = []
        self._resources = []
        return self

    def make(self) -> ClickCaptcha:
        """Create a text-based click captcha instance."""
        opts = default_options()
        for opt in self._opts:
            opt(opts)

        resources = default_resource()
        for resource in self._resources:
            resource(resources)

        return ClickCaptcha(Mode.TEXT, opts, resources)

    def make_shape(self) -> ClickCaptcha:
        """Create a shape-based click captcha instance."""
        opts = default_options()
        opts.thumb_bg_distort = option.DISTORT_LEVEL1
        opts.range_size = option.RangeVal(min_val=24, max_val=30)
        opts.range_thumb_size = option.RangeVal(min_val=14, max_val=20)

        for opt in self._opts:
            opt(opts)

        resources = default_resource()
        for resource in self._resources:
            resource(resources)

        return ClickCaptcha(Mode.SHAPE, opts, resources)

    @staticmethod
    def with_font_dpi(val: int) -> Callable[[Options], None]:
        """Return a mutator that sets the font DPI."""

        def fn(opts: Options):
            opts.font_dpi = max(val, 1)

        return fn

    @staticmethod
    def with_range_len(val: option.RangeVal) -> Callable[[Options], None]:
        """Return a mutator that sets the random content length range."""

        def fn(opts: Options):
            opts.range_len = val

        return fn

    @staticmethod
    def with_range_verify_len(val: option.RangeVal) -> Callable[[Options], None]:
        """Return a mutator that sets the verification content length range."""

        def fn(opts: Options):
            opts.range_verify_len = val

        return fn

    @staticmethod
    def with_disabled_range_verify_len(val: bool) -> Callable[[Options], None]:
        """Return a mutator that disables verification length truncation."""

        def fn(opts: Options):
            opts.disabled_range_verify_len = val

        return fn

    @staticmethod
    def with_image_size(val: option.Size) -> Callable[[Options], None]:
        """Return a mutator that sets the main image size."""

        def fn(opts: Options):
            opts.image_size = val

        return fn

    @staticmethod
    def with_range_size(val: option.RangeVal) -> Callable[[Options], None]:
        """Return a mutator that sets the random content size range."""

        def fn(opts: Options):
            opts.range_size = val

        return fn

    @staticmethod
    def with_range_angle_pos(vals: List[option.RangeVal]) -> Callable[[Options], None]:
        """Return a mutator that sets the random rotation angle ranges."""

        def fn(opts: Options):
            opts.range_angle_pos = vals

        return fn

    @staticmethod
    def with_range_colors(colors: List[str]) -> Callable[[Options], None]:
        """Return a mutator that sets the random text or shape colors."""

        def fn(opts: Options):
            if len(colors) <= 255:
                opts.range_colors = colors

        return fn

    @staticmethod
    def with_display_shadow(val: bool) -> Callable[[Options], None]:
        """Return a mutator that toggles text shadow rendering."""

        def fn(opts: Options):
            opts.display_shadow = val

        return fn

    @staticmethod
    def with_shadow_color(val: str) -> Callable[[Options], None]:
        """Return a mutator that sets the shadow color."""

        def fn(opts: Options):
            opts.shadow_color = val

        return fn

    @staticmethod
    def with_shadow_point(val: option.Point) -> Callable[[Options], None]:
        """Return a mutator that sets the shadow offset."""

        def fn(opts: Options):
            opts.shadow_point = val

        return fn

    @staticmethod
    def with_image_alpha(val: float) -> Callable[[Options], None]:
        """Return a mutator that sets the main image alpha."""

        def fn(opts: Options):
            opts.image_alpha = val

        return fn

    @staticmethod
    def with_range_thumb_size(val: option.RangeVal) -> Callable[[Options], None]:
        """Return a mutator that sets the thumbnail content size range."""

        def fn(opts: Options):
            opts.range_thumb_size = val

        return fn

    @staticmethod
    def with_range_thumb_colors(colors: List[str]) -> Callable[[Options], None]:
        """Return a mutator that sets the thumbnail foreground colors."""

        def fn(opts: Options):
            if len(colors) <= 255:
                opts.range_thumb_colors = colors

        return fn

    @staticmethod
    def with_range_thumb_bg_colors(colors: List[str]) -> Callable[[Options], None]:
        """Return a mutator that sets the thumbnail background colors."""

        def fn(opts: Options):
            if len(colors) <= 255:
                opts.range_thumb_bg_colors = colors

        return fn

    @staticmethod
    def with_thumb_image_size(val: option.Size) -> Callable[[Options], None]:
        """Return a mutator that sets the thumbnail image size."""

        def fn(opts: Options):
            opts.thumb_image_size = val

        return fn

    @staticmethod
    def with_thumb_bg_distort(val: int) -> Callable[[Options], None]:
        """Return a mutator that sets the thumbnail background distortion level."""

        def fn(opts: Options):
            opts.thumb_bg_distort = val

        return fn

    @staticmethod
    def with_thumb_bg_circles_num(val: int) -> Callable[[Options], None]:
        """Return a mutator that sets the thumbnail background circle count."""

        def fn(opts: Options):
            opts.thumb_bg_circles_num = max(val, 0)

        return fn

    @staticmethod
    def with_thumb_bg_slim_line_num(val: int) -> Callable[[Options], None]:
        """Return a mutator that sets the thumbnail background line count."""

        def fn(opts: Options):
            opts.thumb_bg_slim_line_num = max(val, 0)

        return fn

    @staticmethod
    def with_is_thumb_non_deform_ability(val: bool) -> Callable[[Options], None]:
        """Return a mutator that preserves thumbnail background aspect ratio."""

        def fn(opts: Options):
            opts.is_thumb_non_deform_ability = val

        return fn

    @staticmethod
    def with_thumb_disturb_alpha(val: float) -> Callable[[Options], None]:
        """Return a mutator that sets the thumbnail disturbance alpha."""

        def fn(opts: Options):
            opts.thumb_disturb_alpha = val

        return fn

    @staticmethod
    def with_use_shape_original_color(val: bool) -> Callable[[Options], None]:
        """Return a mutator that preserves source colors in shape mode."""

        def fn(opts: Options):
            opts.use_shape_original_color = val

        return fn

    @staticmethod
    def with_chars(chars: List[str]) -> Callable[[Resources], None]:
        """Return a mutator that sets the text seed characters."""

        def fn(resources: Resources):
            resources.chars = chars

        return fn

    @staticmethod
    def with_shapes(shape_maps: Dict[str, Image.Image]) -> Callable[[Resources], None]:
        """Return a mutator that sets the shape seed mapping."""

        def fn(resources: Resources):
            resources.shape_maps = shape_maps
            resources.shapes = list(shape_maps.keys())

        return fn

    @staticmethod
    def with_fonts(fonts: List) -> Callable[[Resources], None]:
        """Return a mutator that sets the available fonts."""

        def fn(resources: Resources):
            resources.rang_fonts = fonts

        return fn

    @staticmethod
    def with_backgrounds(images: List[Image.Image]) -> Callable[[Resources], None]:
        """Return a mutator that sets the main background images."""

        def fn(resources: Resources):
            resources.rang_backgrounds = images

        return fn

    @staticmethod
    def with_thumb_backgrounds(images: List[Image.Image]) -> Callable[[Resources], None]:
        """Return a mutator that sets the thumbnail background images."""

        def fn(resources: Resources):
            resources.rang_thumb_backgrounds = images

        return fn
