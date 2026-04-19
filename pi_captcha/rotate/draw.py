"""
Rotate captcha image rendering

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""
from typing import Optional
from PIL import Image
from pi_captcha.base import helper


class DrawImage:
    """Image renderer"""

    def _center_crop(self, image: Image.Image, target_width: int, target_height: int) -> Image.Image:
        """Center crop to the requested size"""
        if image.size == (target_width, target_height):
            return image

        width, height = image.size
        if width < target_width or height < target_height:
            scale = max(target_width / max(width, 1), target_height / max(height, 1))
            resized_width = max(target_width, int(round(width * scale)))
            resized_height = max(target_height, int(round(height * scale)))
            image = image.resize((resized_width, resized_height), Image.Resampling.LANCZOS)
            width, height = image.size

        left = max(0, (width - target_width) // 2)
        top = max(0, (height - target_height) // 2)
        right = left + target_width
        bottom = top + target_height
        return image.crop((left, top, right, bottom))

    def draw_with_nrgba(self, square_size: int, background: Optional[Image.Image]) -> Image.Image:
        """
        Render an image using RGBA mode

        The background is only randomly cropped and resized, not rotated
        """
        if background:
            if background.size == (square_size, square_size) and background.mode == "RGBA":
                return background.copy()

            return helper.random_crop_resize(background, square_size, square_size)

        return Image.new("RGBA", (square_size, square_size), (255, 255, 255, 255))

    def draw_with_crop_circle(self, background: Image.Image, alpha: float,
                             square_size: int, rotate: int,
                             scale_ratio_size: int) -> Image.Image:
        """Render a circular cropped thumbnail"""
        mask = helper.create_anti_aliased_ellipse_mask(square_size, square_size)

        # Crop a circular region from the background
        center_x = background.width // 2
        center_y = background.height // 2

        crop_size = square_size + scale_ratio_size * 2

        # Calculate the crop rectangle
        left = center_x - crop_size // 2
        top = center_y - crop_size // 2
        right = left + crop_size
        bottom = top + crop_size

        # Clamp bounds and pad with transparency when needed so the crop stays square
        src_left = max(0, left)
        src_top = max(0, top)
        src_right = min(background.width, right)
        src_bottom = min(background.height, bottom)

        cropped = Image.new("RGBA", (crop_size, crop_size), (0, 0, 0, 0))
        background_rgba = background if background.mode == "RGBA" else background.convert("RGBA")
        src_crop = background_rgba.crop((src_left, src_top, src_right, src_bottom))
        paste_x = src_left - left
        paste_y = src_top - top
        cropped.paste(src_crop, (paste_x, paste_y))

        if rotate != 0:
            rotate = rotate % 360
            if rotate != 0:
                cropped = helper.high_quality_rotate(cropped, rotate)

        cropped = self._center_crop(cropped, square_size, square_size)

        if alpha < 1.0:
            alpha_channel = cropped.split()[3]
            alpha_channel = alpha_channel.point(lambda p: int(p * alpha))
            cropped.putalpha(alpha_channel)

        result = Image.new("RGBA", (square_size, square_size), (0, 0, 0, 0))
        result.paste(cropped, (0, 0), mask)

        return result

