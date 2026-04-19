"""
Core click captcha generation logic

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""
from typing import Dict, List, Tuple
from PIL import Image, ImageDraw
from pi_captcha.base import option, random as base_random, helper, randgen
from pi_captcha.base import imagedata
from pi_captcha.click.dot import Dot
from pi_captcha.click.draw import DrawImage, DrawDot
from pi_captcha.click.data import CaptData
from pi_captcha.click.option import Options
from pi_captcha.click.resource import Resources


class Mode:
    """Mode constants"""
    TEXT = 0
    SHAPE = 1


class Captcha:
    """Captcha interface"""
    def get_options(self) -> Options:
        """Return active options"""
        raise NotImplementedError
    
    def generate(self) -> CaptData:
        """Generate captcha data"""
        raise NotImplementedError


class ClickCaptcha(Captcha):
    """Click captcha implementation"""
    
    def __init__(self, mode: int, opts: Options, resources: Resources):
        self.mode = mode
        self.opts = opts
        self.resources = resources
        self.draw_image = DrawImage()
    
    def get_options(self) -> Options:
        """Return active options"""
        return self.opts
    
    def generate(self) -> CaptData:
        """Generate captcha data"""
        if self.mode == Mode.SHAPE:
            return self._generate_with_shape()
        return self._generate_with_text()
    
    def _generate_with_text(self) -> CaptData:
        """Generate a text-based click captcha."""
        self._check()
        
        chars = self._gen_chars()
        dots = self._gen_dots(self.opts.image_size, self.opts.range_size, chars, 10)
        verify_dots, verify_shapes = self._range_check_dots(dots)
        thumb_dots = self._gen_dots(self.opts.thumb_image_size, self.opts.range_thumb_size,
                                    verify_shapes, 0)
        
        master_image = self._gen_master_image(self.opts.image_size, dots)
        thumb_image = self._gen_thumb_image(self.opts.thumb_image_size, thumb_dots)
        
        return CaptData(
            dots=verify_dots,
            master_image=imagedata.JPEGImageData(master_image),
            thumb_image=imagedata.PNGImageData(thumb_image)
        )
    
    def _generate_with_shape(self) -> CaptData:
        """Generate a shape-based click captcha."""
        self._check()
        
        shapes = self._gen_shapes()
        dots = self._gen_dots(self.opts.image_size, self.opts.range_size, shapes, 10)
        verify_dots, verify_shapes = self._range_check_dots(dots)
        thumb_dots = self._gen_dots(self.opts.thumb_image_size, self.opts.range_thumb_size,
                                    verify_shapes, 0)
        
        master_image = self._gen_master_image(self.opts.image_size, dots)
        thumb_image = self._gen_thumb_image(self.opts.thumb_image_size, thumb_dots)
        
        return CaptData(
            dots=verify_dots,
            master_image=imagedata.JPEGImageData(master_image),
            thumb_image=imagedata.PNGImageData(thumb_image)
        )
    
    def _check(self):
        """Validate required resources and option constraints."""
        if self.mode == Mode.TEXT:
            if len(self.resources.chars) < self.opts.range_len.max:
                raise ValueError("character set length must be greater than range_len.max")
        elif self.mode == Mode.SHAPE:
            if len(self.resources.shapes) < self.opts.range_len.max:
                raise ValueError("shape set length must be greater than range_len.max")
            for img in self.resources.shape_maps.values():
                if img is None:
                    raise ValueError("shape resources must contain valid images")
        
        if len(self.resources.rang_backgrounds) == 0:
            raise ValueError("background images cannot be empty")
    
    def _gen_chars(self) -> List[str]:
        """Generate a random list of characters."""
        length = base_random.rand_int(self.opts.range_len.min, self.opts.range_len.max)
        return self._gen_rand_char(length)
    
    def _gen_shapes(self) -> List[str]:
        """Generate a random list of shapes."""
        length = base_random.rand_int(self.opts.range_len.min, self.opts.range_len.max)
        return self._gen_rand_shape(length)
    
    def _gen_rand_char(self, length: int) -> List[str]:
        """
Generate a random character array efficiently.

Use `random.sample` to avoid duplicates and inefficient retry loops.
"""
        if length <= 0:
            return []
        
        chars = self.resources.chars
        if not chars:
            return []
        
        from pi_captcha.base.thread_random import get_thread_random
        rng = get_thread_random()
        
        # If the requested length is greater than or equal to the character set size, return all shuffled characters
        if length >= len(chars):
            result = chars.copy()
            rng.shuffle(result)
            return result
        
        # Use random.sample for efficient non-repeating sampling
        return rng.sample(chars, length)
    
    def _gen_rand_shape(self, length: int) -> List[str]:
        """
Generate a random shape array efficiently.

Use `random.sample` to avoid duplicates and inefficient retry loops.
"""
        if length <= 0:
            return []
        
        shapes = self.resources.shapes
        if not shapes:
            return []
        
        from pi_captcha.base.thread_random import get_thread_random
        rng = get_thread_random()
        
        # If the requested length is greater than or equal to the shape set size, return all shuffled shapes
        if length >= len(shapes):
            result = shapes.copy()
            rng.shuffle(result)
            return result
        
        # Use random.sample for efficient non-repeating sampling
        return rng.sample(shapes, length)
    
    def _gen_dots(self, image_size: option.Size, size: option.RangeVal,
                  values: List[str], padding: int) -> Dict[int, Dot]:
        """Generate dot metadata."""
        dots = {}
        width = image_size.width
        height = image_size.height
        if padding > 0:
            width -= padding
            height -= padding
        
        length = len(values)
        for i in range(length):
            value = values[i]
            rand_angle = self._rand_angle()
            rand_color = randgen.rand_hex_color(self.opts.range_colors)
            rand_color2 = randgen.rand_hex_color(self.opts.range_thumb_colors)
            rand_size = base_random.rand_int(size.min, size.max)
            c_height = rand_size
            c_width = rand_size
            
            if self.mode == Mode.TEXT and helper.len_chinese_char(value) > 1:
                c_width = rand_size * helper.len_chinese_char(value)
                if rand_angle > 0:
                    surplus = c_width - rand_size
                    ra = rand_angle % 90
                    pr = float(surplus) / 90
                    r = max(float(ra) * pr, 1)
                    c_height = c_height + int(r)
                    c_width = c_width + int(r)
            
            dy = 10
            w = width // length
            rd = abs(float(w) - float(c_width))
            xx = (i * w) + base_random.rand_int(0, int(max(rd, 1)))
            yy = base_random.rand_int(dy, height + c_height)
            
            x = int(min(max(float(xx), float(dy)), float(width - dy - (padding * 2))))
            y = int(min(max(float(yy), float(c_height + dy)),
                       float(height + (c_height // 2) - (padding * 2))))
            
            dot = Dot()
            dot.index = i
            dot.x = x
            dot.y = y - c_height
            dot.size = rand_size
            dot.width = c_width
            dot.height = c_height
            dot.angle = rand_angle
            dot.color = rand_color
            dot.color2 = rand_color2
            
            if self.mode == Mode.SHAPE:
                dot.shape = value
            else:
                dot.text = value
            
            dots[i] = dot
        
        return dots
    
    def _range_check_dots(self, dots: Dict[int, Dot]) -> Tuple[Dict[int, Dot], List[str]]:
        """Select random verification dots."""
        rs = base_random.perm(len(dots))
        chk_dots = {}
        count = base_random.rand_int(self.opts.range_verify_len.min,
                                    self.opts.range_verify_len.max)
        values = []
        
        for i, value in enumerate(rs):
            if not self.opts.disabled_range_verify_len and i >= count:
                break
            
            dot = dots[value]
            dot.index = i
            chk_dots[i] = dot
            if self.mode == Mode.SHAPE:
                values.append(chk_dots[i].shape)
            else:
                values.append(chk_dots[i].text)
        
        return chk_dots, values
    
    def _gen_master_image(self, size: option.Size, dots: Dict[int, Dot]) -> Image.Image:
        """Render the main captcha image."""
        draw_dots = []
        
        for i in range(len(dots)):
            dot = dots[i]
            draw_dot = DrawDot()
            draw_dot.dot = dot
            draw_dot.x = dot.x
            draw_dot.y = dot.y
            draw_dot.width = dot.width
            draw_dot.height = dot.height
            draw_dot.angle = dot.angle
            draw_dot.color = dot.color
            draw_dot.size = dot.size
            
            if self.mode == Mode.SHAPE:
                draw_dot.draw_type = "image"
                if dot.shape in self.resources.shape_maps:
                    draw_dot.image = self.resources.shape_maps[dot.shape]
                draw_dot.use_original_color = self.opts.use_shape_original_color
            else:
                draw_dot.draw_type = "string"
                draw_dot.text = dot.text
                draw_dot.font_dpi = self.opts.font_dpi
                draw_dot.font = randgen.rand_font(self.resources.rang_fonts)
            
            draw_dots.append(draw_dot)
        
        return self.draw_image.draw_with_nrgba(
            width=size.width,
            height=size.height,
            background=randgen.rand_image(self.resources.rang_backgrounds),
            alpha=self.opts.image_alpha,
            draw_dots=draw_dots,
            show_shadow=self.opts.display_shadow,
            shadow_color=self.opts.shadow_color,
            shadow_point=self.opts.shadow_point
        )
    
    def _gen_thumb_background(self, size: option.Size) -> Image.Image:
        """Generate the thumbnail background using colors, images, and noise options."""
        bg = randgen.rand_image(self.resources.rang_thumb_backgrounds)
        if bg:
            if self.opts.is_thumb_non_deform_ability:
                thumb_bg = helper.random_crop_resize(bg, size.width, size.height)
            else:
                thumb_bg = bg.convert("RGBA").resize((size.width, size.height), Image.Resampling.LANCZOS)
        else:
            background_colors = self.opts.range_thumb_bg_colors or self.opts.range_thumb_colors or ["#ffffff"]
            base_color = randgen.rand_hex_color(background_colors)
            try:
                r, g, b, a = helper.parse_hex_color(base_color)
                thumb_bg = Image.new("RGBA", (size.width, size.height), (r, g, b, a))
            except Exception:
                thumb_bg = Image.new("RGBA", (size.width, size.height), (255, 255, 255, 255))

        distort_level = max(int(self.opts.thumb_bg_distort), 0)
        if distort_level <= option.DISTORT_NONE:
            return thumb_bg

        draw = ImageDraw.Draw(thumb_bg, "RGBA")
        colors = self.opts.range_thumb_bg_colors or self.opts.range_thumb_colors or self.opts.range_colors or ["#cccccc"]
        circles_num = max(0, int(round(self.opts.thumb_bg_circles_num * distort_level / option.DISTORT_LEVEL4)))
        line_num = max(0, int(round(self.opts.thumb_bg_slim_line_num * distort_level / option.DISTORT_LEVEL4)))

        for _ in range(circles_num):
            radius = base_random.rand_int(2, max(3, min(size.width, size.height) // 5))
            x = base_random.rand_int(-radius, size.width)
            y = base_random.rand_int(-radius, size.height)
            color = randgen.rand_hex_color(colors)
            try:
                r, g, b, _ = helper.parse_hex_color(color)
                fill = (r, g, b, 50 + min(120, distort_level * 18))
            except Exception:
                fill = (220, 220, 220, 80)
            draw.ellipse((x, y, x + radius, y + radius), fill=fill)

        for _ in range(line_num):
            color = randgen.rand_hex_color(colors)
            try:
                r, g, b, _ = helper.parse_hex_color(color)
                fill = (r, g, b, 70 + min(100, distort_level * 15))
            except Exception:
                fill = (180, 180, 180, 90)
            y = base_random.rand_int(0, max(size.height - 1, 0))
            x1 = base_random.rand_int(0, max(size.width - 1, 0))
            x2 = base_random.rand_int(0, max(size.width - 1, 0))
            draw.line((x1, y, x2, y), fill=fill, width=1)

        return thumb_bg

    def _gen_thumb_image(self, size: option.Size, dots: Dict[int, Dot]) -> Image.Image:
        """Render the thumbnail image."""
        draw_dots = []

        width = size.width // len(dots) if len(dots) > 0 else size.width
        for i in range(len(dots)):
            dot = dots[i]
            length = 1
            if self.mode == Mode.TEXT:
                length = max(len(dot.text), 1)

            cell_left = width * i
            cell_center_x = cell_left + width // 2
            dx = max(cell_center_x - dot.width // 2, 8)

            # Use a thread-safe random generator
            from pi_captcha.base.thread_random import get_thread_random
            rng = get_thread_random()
            vertical_jitter = max(size.height // 12, 1)
            dy = max((size.height - dot.height) // 2 - rng.randint(0, vertical_jitter * length // 2), 0)

            draw_dot = DrawDot()
            draw_dot.dot = dot
            draw_dot.x = dx
            draw_dot.y = dy
            draw_dot.angle = dot.angle
            draw_dot.color = dot.color2
            draw_dot.size = dot.size
            draw_dot.width = dot.width
            draw_dot.height = dot.height

            if self.mode == Mode.SHAPE:
                draw_dot.draw_type = "image"
                if dot.shape in self.resources.shape_maps:
                    draw_dot.image = self.resources.shape_maps[dot.shape]
                draw_dot.use_original_color = self.opts.use_shape_original_color
            else:
                draw_dot.draw_type = "string"
                draw_dot.text = dot.text
                draw_dot.font_dpi = self.opts.font_dpi
                draw_dot.font = randgen.rand_font(self.resources.rang_fonts)

            draw_dots.append(draw_dot)
        
        thumb_bg = self._gen_thumb_background(size)
        
        return self.draw_image.draw_with_nrgba(
            width=size.width,
            height=size.height,
            background=thumb_bg,
            alpha=self.opts.thumb_disturb_alpha,
            draw_dots=draw_dots
        )
    
    def _rand_angle(self) -> int:
        """Generate a random angle."""
        angles = self.opts.range_angle_pos
        index = helper.rand_index(len(angles))
        if index < 0:
            return 0
        
        angle = angles[index]
        return base_random.rand_int(angle.min, angle.max)

