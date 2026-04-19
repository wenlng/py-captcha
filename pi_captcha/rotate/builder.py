"""
Builder utilities for rotate captcha generation.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

from typing import Callable, List

from PIL import Image

from pi_captcha.base import option
from pi_captcha.rotate.option import Options, default_options
from pi_captcha.rotate.resource import Resources, default_resource
from pi_captcha.rotate.rotate import RotateCaptcha


class RotateBuilder:
    """Builder for configuring and creating rotate captchas."""

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

    def make(self) -> RotateCaptcha:
        """Create a rotate captcha instance."""
        opts = default_options()
        for opt in self._opts:
            opt(opts)
        resources = default_resource()
        for resource in self._resources:
            resource(resources)
        return RotateCaptcha(opts, resources)

    @staticmethod
    def with_image_square_size(val: int) -> Callable[[Options], None]:
        """Return a mutator that sets the main image square size."""

        def fn(opts: Options):
            opts.image_square_size = val

        return fn

    @staticmethod
    def with_range_angle_pos(vals: List[option.RangeVal]) -> Callable[[Options], None]:
        """Return a mutator that sets the allowed rotation angle ranges."""

        def fn(opts: Options):
            opts.range_angle_pos = vals

        return fn

    @staticmethod
    def with_range_thumb_image_square_size(val: List[int]) -> Callable[[Options], None]:
        """Return a mutator that sets the thumbnail square sizes."""

        def fn(opts: Options):
            opts.range_thumb_image_square_size = val

        return fn

    @staticmethod
    def with_thumb_image_alpha(val: float) -> Callable[[Options], None]:
        """Return a mutator that sets the thumbnail alpha."""

        def fn(opts: Options):
            opts.thumb_image_alpha = val

        return fn

    @staticmethod
    def with_images(images: List[Image.Image]) -> Callable[[Resources], None]:
        """Return a mutator that sets the source images."""

        def fn(resources: Resources):
            resources.rang_images = images

        return fn
