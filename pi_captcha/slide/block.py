"""
Block models for slide captcha generation.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""


class Block:
    """Block metadata for slide captcha results."""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.angle = 0
        self.tile_x = 0
        self.tile_y = 0
        self.dx = 0
        self.dy = 0


class GraphImage:
    """Container for overlay, shadow, and mask images."""

    def __init__(self):
        self.overlay_image = None
        self.shadow_image = None
        self.mask_image = None
