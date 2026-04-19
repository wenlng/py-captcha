"""
Click captcha image rendering helpers.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

import os
from typing import List, Optional

from PIL import Image, ImageChops, ImageDraw, ImageFont

from pi_captcha.base import helper
from pi_captcha.click.dot import Dot


class DrawDot:
    """Drawable dot metadata."""

    def __init__(self):
        self.dot: Optional[Dot] = None
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.angle = 0
        self.color = ""
        self.size = 0
        self.text = ""
        self.shape = ""
        self.image: Optional[Image.Image] = None
        self.font = None
        self.font_dpi = 72
        self.use_original_color = False
        self.draw_type = "string"


class DrawImage:
    """Image renderer for click captchas."""

    def _load_font(self, font_source, font_size: int, font_dpi: int = 72):
        """Load a font from a path or Pillow font object."""
        effective_size = max(1, int(round(font_size * max(font_dpi, 1) / 72)))
        try:
            if isinstance(font_source, (str, os.PathLike)):
                return ImageFont.truetype(str(font_source), effective_size)
            if font_source is not None and hasattr(font_source, "getbbox"):
                return font_source
        except Exception:
            pass
        return ImageFont.load_default()

    def _apply_shape_color(self, image: Image.Image, color: str, use_original_color: bool) -> Image.Image:
        """Apply tinting unless original shape colors should be preserved."""
        if use_original_color:
            return image
        try:
            r, g, b, _ = helper.parse_hex_color(color)
        except Exception:
            return image
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        alpha = image.getchannel("A")
        tinted = Image.new("RGBA", image.size, (r, g, b, 255))
        tinted.putalpha(alpha)
        base_luminance = image.convert("L")
        tinted_rgb = tinted.convert("RGB")
        shaded_rgb = ImageChops.multiply(
            tinted_rgb,
            Image.merge("RGB", (base_luminance, base_luminance, base_luminance)),
        )
        return Image.merge("RGBA", (*shaded_rgb.split(), alpha))

    def _trim_transparent_edges(self, image: Image.Image) -> Image.Image:
        """Trim transparent edges before fitting the shape."""
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        alpha = image.getchannel("A")
        bbox = alpha.getbbox()
        if bbox is None:
            return image
        return image.crop(bbox)

    def _fit_image_to_box(self, image: Image.Image, target_size: tuple[int, int]) -> Image.Image:
        """Fit an image into a target box while preserving aspect ratio."""
        target_width, target_height = target_size
        if target_width <= 0 or target_height <= 0:
            return image
        source_width, source_height = image.size
        if source_width <= 0 or source_height <= 0:
            return Image.new("RGBA", target_size, (0, 0, 0, 0))
        scale = min(target_width / source_width, target_height / source_height)
        resized_width = max(1, int(round(source_width * scale)))
        resized_height = max(1, int(round(source_height * scale)))
        resized = image.resize((resized_width, resized_height), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", target_size, (0, 0, 0, 0))
        offset_x = (target_width - resized_width) // 2
        offset_y = (target_height - resized_height) // 2
        canvas.paste(resized, (offset_x, offset_y), resized)
        return canvas

    def draw_with_nrgba(
        self,
        width: int,
        height: int,
        background: Optional[Image.Image],
        alpha: float,
        draw_dots: List[DrawDot],
        show_shadow: bool = False,
        shadow_color: str = "#101010",
        shadow_point: Optional = None,
    ) -> Image.Image:
        """Render the click captcha image using RGBA mode."""
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
        draw = ImageDraw.Draw(img)
        for draw_dot in draw_dots:
            if draw_dot.draw_type == "string":
                self._draw_text(img, draw, draw_dot, show_shadow, shadow_color, shadow_point)
            elif draw_dot.draw_type == "image":
                self._draw_image(img, draw_dot)
        return img

    def _draw_text(
        self,
        img: Image.Image,
        draw: ImageDraw.ImageDraw,
        draw_dot: DrawDot,
        show_shadow: bool,
        shadow_color: str,
        shadow_point: Optional,
    ):
        """Draw text content onto the image."""
        if not draw_dot.text:
            return
        font_size = draw_dot.size
        font = self._load_font(draw_dot.font, font_size, draw_dot.font_dpi)
        bbox = draw.textbbox((0, 0), draw_dot.text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = draw_dot.x
        y = draw_dot.y
        try:
            r, g, b, a = helper.parse_hex_color(draw_dot.color)
            fill_color = (r, g, b, a)
        except Exception:
            fill_color = (0, 0, 0, 255)
        if draw_dot.angle != 0:
            temp_img = Image.new("RGBA", (text_width + 40, text_height + 40), (0, 0, 0, 0))
            temp_draw = ImageDraw.Draw(temp_img)
            if show_shadow:
                shadow_x = 20 + (shadow_point.x if shadow_point else -1)
                shadow_y = 20 + (shadow_point.y if shadow_point else -1)
                temp_draw.text((shadow_x, shadow_y), draw_dot.text, fill=shadow_color, font=font)
            temp_draw.text((20, 20), draw_dot.text, fill=fill_color, font=font)
            rotated = helper.high_quality_rotate(temp_img, draw_dot.angle)
            rot_width, rot_height = rotated.size
            center_x = x + text_width // 2
            center_y = y + text_height // 2
            paste_x = center_x - rot_width // 2
            paste_y = center_y - rot_height // 2
            img.paste(rotated, (paste_x, paste_y), rotated)
        else:
            if show_shadow:
                shadow_x = x + (shadow_point.x if shadow_point else -1)
                shadow_y = y + (shadow_point.y if shadow_point else -1)
                draw.text((shadow_x, shadow_y), draw_dot.text, fill=shadow_color, font=font)
            draw.text((x, y), draw_dot.text, fill=fill_color, font=font)

    def _draw_image(self, img: Image.Image, draw_dot: DrawDot):
        """Draw image content onto the image."""
        if not draw_dot.image:
            return
        source_image = self._trim_transparent_edges(draw_dot.image)
        source_image = self._apply_shape_color(source_image, draw_dot.color, draw_dot.use_original_color)
        target_size = (draw_dot.width, draw_dot.height)
        rendered = self._fit_image_to_box(source_image, target_size)
        if draw_dot.angle != 0:
            rendered = helper.high_quality_rotate(rendered, draw_dot.angle)
        img.paste(rendered, (draw_dot.x, draw_dot.y), rendered if rendered.mode == "RGBA" else None)
