"""
Builder utilities for slide captcha generation.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

from typing import Callable, List

from PIL import Image

from pi_captcha.base import option
from pi_captcha.slide.block import GraphImage
from pi_captcha.slide.option import DeadZoneDirectionType, Options, default_options
from pi_captcha.slide.resource import Resources, default_resource
from pi_captcha.slide.slide import Mode, SlideCaptcha


class SlideBuilder:
    """Builder for configuring and creating slide captchas."""

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

    def make(self) -> SlideCaptcha:
        """Create a basic slide captcha instance."""
        opts = default_options()
        opts.range_dead_zone_directions = [DeadZoneDirectionType.LEFT]
        opts.enable_graph_vertical_random = False
        for opt in self._opts:
            opt(opts)
        resources = default_resource()
        for resource in self._resources:
            resource(resources)
        return SlideCaptcha(Mode.BASIC, opts, resources)

    def make_drag_drop(self) -> SlideCaptcha:
        """Create a drag-and-drop slide captcha instance."""
        opts = default_options()
        for opt in self._opts:
            opt(opts)
        resources = default_resource()
        for resource in self._resources:
            resource(resources)
        return SlideCaptcha(Mode.DRAG, opts, resources)

    @staticmethod
    def with_image_size(val: option.Size) -> Callable[[Options], None]:
        """Return a mutator that sets the main image size."""

        def fn(opts: Options):
            opts.image_size = val

        return fn

    @staticmethod
    def with_image_alpha(val: float) -> Callable[[Options], None]:
        """Return a mutator that sets the main image alpha."""

        def fn(opts: Options):
            opts.image_alpha = val

        return fn

    @staticmethod
    def with_range_graph_size(val: option.RangeVal) -> Callable[[Options], None]:
        """Return a mutator that sets the graph size range."""

        def fn(opts: Options):
            opts.range_graph_size = val

        return fn

    @staticmethod
    def with_range_graph_angle_pos(vals: List[option.RangeVal]) -> Callable[[Options], None]:
        """Return a mutator that sets the graph angle ranges."""

        def fn(opts: Options):
            opts.range_graph_angle_pos = vals

        return fn

    @staticmethod
    def with_gen_graph_number(val: int) -> Callable[[Options], None]:
        """Return a mutator that sets the number of graph blocks."""

        def fn(opts: Options):
            opts.gen_graph_number = 1 if val <= 1 else val

        return fn

    @staticmethod
    def with_enable_graph_vertical_random(val: bool) -> Callable[[Options], None]:
        """Return a mutator that toggles vertical randomness for graph placement."""

        def fn(opts: Options):
            opts.enable_graph_vertical_random = val

        return fn

    @staticmethod
    def with_range_dead_zone_directions(val: List[int]) -> Callable[[Options], None]:
        """Return a mutator that sets the dead-zone directions."""

        def fn(opts: Options):
            opts.range_dead_zone_directions = val

        return fn

    @staticmethod
    def with_backgrounds(images: List[Image.Image]) -> Callable[[Resources], None]:
        """Return a mutator that sets the main background images."""

        def fn(resources: Resources):
            resources.rang_backgrounds = images

        return fn

    @staticmethod
    def with_graph_images(graph_images: List[GraphImage]) -> Callable[[Resources], None]:
        """Return a mutator that sets the graph image resources."""

        def fn(resources: Resources):
            resources.rang_graph_image = graph_images

        return fn
