"""
Slide captcha image rendering helpers.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

from typing import List, Optional

from PIL import Image

from py_captcha.base import helper
from py_captcha.slide.block import Block


class DrawBlock:
    """Drawable block metadata."""

    def __init__(self):
        self.block: Optional[Block] = None
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.angle = 0
        self.image: Optional[Image.Image] = None


class DrawImage:
    """Image renderer for slide captchas."""

    def draw_with_nrgba(
        self,
        width: int,
        height: int,
        background: Optional[Image.Image],
        alpha: float,
        draw_blocks: List[DrawBlock],
    ) -> Image.Image:
        """Render an image using RGBA mode."""
        if background:
            img = helper.random_crop_resize(background, width, height)
        else:
            img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        if alpha < 1.0:
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            alpha_channel = img.split()[3]
            alpha_channel = alpha_channel.point(lambda p: int(p * alpha))
            img.putalpha(alpha_channel)
        for draw_block in draw_blocks:
            if draw_block.image:
                self._draw_block(img, draw_block)
        return img

    def draw_with_template(
        self,
        background: Image.Image,
        mask_image: Image.Image,
        alpha: float,
        width: int,
        height: int,
        draw_block: DrawBlock,
    ) -> Image.Image:
        """Render a tile image using a mask template."""
        mask_resized = mask_image.resize((width, height), Image.Resampling.LANCZOS).convert("RGBA")
        if draw_block.angle != 0:
            mask_resized = helper.high_quality_rotate(mask_resized, draw_block.angle)
        mask_alpha = mask_resized.getchannel("A")
        tile_width, tile_height = mask_resized.size
        bg_crop = background.crop((
            draw_block.x,
            draw_block.y,
            draw_block.x + width,
            draw_block.y + height,
        )).convert("RGBA")
        if bg_crop.size != (tile_width, tile_height):
            bg_crop = bg_crop.resize((tile_width, tile_height), Image.Resampling.LANCZOS)
        result = Image.new("RGBA", (tile_width, tile_height), (0, 0, 0, 0))
        result.paste(bg_crop, (0, 0), mask_alpha)
        if draw_block.image:
            overlay_resized = draw_block.image.resize((width, height), Image.Resampling.LANCZOS).convert("RGBA")
            if draw_block.angle != 0:
                overlay_resized = helper.high_quality_rotate(overlay_resized, draw_block.angle)
                if overlay_resized.size != (tile_width, tile_height):
                    overlay_resized = overlay_resized.resize((tile_width, tile_height), Image.Resampling.LANCZOS)
            elif overlay_resized.size != (tile_width, tile_height):
                overlay_resized = overlay_resized.resize((tile_width, tile_height), Image.Resampling.LANCZOS)
            tile_overlay = Image.new("RGBA", (tile_width, tile_height), (0, 0, 0, 0))
            tile_overlay.paste(overlay_resized, (0, 0), mask_alpha)
            result.alpha_composite(tile_overlay)
        return result

    def _draw_block(self, img: Image.Image, draw_block: DrawBlock):
        """Draw a block image onto the canvas."""
        if not draw_block.image:
            return
        if draw_block.image.size == (draw_block.width, draw_block.height) and draw_block.angle == 0:
            img.paste(
                draw_block.image,
                (draw_block.x, draw_block.y),
                draw_block.image if draw_block.image.mode == "RGBA" else None,
            )
            return
        target_size = (draw_block.width, draw_block.height)
        resized = draw_block.image.resize(target_size, Image.Resampling.LANCZOS)
        if draw_block.angle != 0:
            resized = helper.high_quality_rotate(resized, draw_block.angle)
        img.paste(resized, (draw_block.x, draw_block.y), resized if resized.mode == "RGBA" else None)
