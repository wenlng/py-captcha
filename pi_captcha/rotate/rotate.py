"""
Core logic for rotate captcha generation.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

from PIL import Image

from pi_captcha.base import helper, imagedata, randgen, random as base_random
from pi_captcha.rotate.block import Block
from pi_captcha.rotate.data import CaptData
from pi_captcha.rotate.draw import DrawImage
from pi_captcha.rotate.option import Options
from pi_captcha.rotate.resource import Resources


class Captcha:
    """Rotate captcha interface."""

    def get_options(self) -> Options:
        """Return active options."""
        raise NotImplementedError

    def generate(self) -> CaptData:
        """Generate captcha data."""
        raise NotImplementedError


class RotateCaptcha(Captcha):
    """Rotate captcha implementation."""

    def __init__(self, opts: Options, resources: Resources):
        self.opts = opts
        self.resources = resources
        self.draw_image = DrawImage()

    def get_options(self) -> Options:
        """Return active options."""
        return self.opts

    def generate(self) -> CaptData:
        """Generate captcha data."""
        self._check()
        thumb_image_square_size = self._rand_thumb_image_square_size()
        block = self._gen_block(self.opts.image_square_size, thumb_image_square_size)
        master_image = self._gen_master_image(self.opts.image_square_size, block)
        thumb_image = self._gen_thumb_image(master_image, block, thumb_image_square_size)
        return CaptData(
            block=block,
            master_image=imagedata.PNGImageData(master_image),
            thumb_image=imagedata.PNGImageData(thumb_image),
        )

    def _check(self):
        """Validate required image resources."""
        if len(self.resources.rang_images) == 0:
            raise ValueError("image resources cannot be empty")
        for img in self.resources.rang_images:
            if img is None:
                raise ValueError("image resources must contain valid images")

    def _gen_master_image(self, size: int, block: Block) -> Image.Image:
        """Generate the main image."""
        return self.draw_image.draw_with_nrgba(square_size=size, background=randgen.rand_image(self.resources.rang_images))

    def _gen_thumb_image(self, bg_image: Image.Image, block: Block, thumb_image_square_size: int) -> Image.Image:
        """Generate the thumbnail image."""
        return self.draw_image.draw_with_crop_circle(
            background=bg_image,
            alpha=self.opts.thumb_image_alpha,
            square_size=thumb_image_square_size,
            rotate=block.angle,
            scale_ratio_size=(self.opts.image_square_size - thumb_image_square_size) // 2,
        )

    def _rand_angle(self) -> int:
        """Generate a random angle."""
        angles = self.opts.range_angle_pos
        index = helper.rand_index(len(angles))
        if index < 0:
            return 0
        angle = angles[index]
        return base_random.rand_int(angle.min, angle.max)

    def _rand_thumb_image_square_size(self) -> int:
        """Generate a random thumbnail size."""
        size = self.opts.range_thumb_image_square_size
        index = helper.rand_index(len(size))
        if index < 0:
            return 0
        return size[index]

    def _gen_block(self, image_size: int, thumb_image_square_size: int) -> Block:
        """Generate block metadata for the rotate captcha."""
        block = Block()
        block.angle = self._rand_angle()
        block.width = thumb_image_square_size
        block.height = thumb_image_square_size
        block.parent_width = image_size
        block.parent_height = image_size
        return block
