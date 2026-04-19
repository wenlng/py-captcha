"""
Core slide captcha logic

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""
from typing import List, Optional, Tuple
from PIL import Image
from py_captcha.base import option, random as base_random, helper, randgen
from py_captcha.base import imagedata
from py_captcha.slide.block import Block, GraphImage
from py_captcha.slide.draw import DrawImage, DrawBlock
from py_captcha.slide.data import CaptData
from py_captcha.slide.option import Options, DeadZoneDirectionType
from py_captcha.slide.resource import Resources


class Mode:
    """Mode constants"""
    BASIC = 0
    DRAG = 1


class Captcha:
    """Captcha interface"""
    def get_options(self) -> Options:
        """Return active options"""
        raise NotImplementedError
    
    def generate(self) -> CaptData:
        """Generate captcha data"""
        raise NotImplementedError


class SlideCaptcha(Captcha):
    """Slide captcha implementation"""
    
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
        self._check()
        
        overlay_image, shadow_image, mask_image = self._gen_graph()
        if overlay_image is None or shadow_image is None or mask_image is None:
            raise ValueError("graph images are invalid")
        
        blocks, tile_point = self._gen_graph_blocks(
            self.opts.image_size,
            self.opts.range_graph_size,
            self.opts.gen_graph_number
        )
        
        if len(blocks) > 1:
            index = helper.rand_index(len(blocks))
            if index < 0:
                index = 0
            block = blocks[index]
        else:
            block = blocks[0]
        
        if block is None:
            raise ValueError("failed to generate captcha data")
        
        master_image, master_bg_image = self._gen_master_image(
            self.opts.image_size, shadow_image, blocks
        )
        tile_image = self._gen_tile_image(mask_image, master_bg_image, overlay_image, block)

        target_x = block.x
        target_y = block.y
        if self.mode == Mode.BASIC:
            block.tile_y = block.y
        else:
            block.tile_y = tile_point.y

        block.tile_x = tile_point.x
        block.dx = target_x
        block.dy = target_y
        
        return CaptData(
            block=block,
            master_image=imagedata.JPEGImageData(master_image),
            tile_image=imagedata.PNGImageData(tile_image)
        )
    
    def _check(self):
        """Validate required resources"""
        for tile in self.resources.rang_graph_image:
            if tile.overlay_image is None:
                raise ValueError("puzzle overlay images must be valid images")
            elif tile.shadow_image is None:
                raise ValueError("puzzle shadow images must be valid images")
            elif tile.mask_image is None:
                raise ValueError("puzzle mask images must be valid images")
        
        if len(self.resources.rang_backgrounds) == 0:
            raise ValueError("background images cannot be empty")
    
    def _gen_graph(self) -> Tuple[Optional[Image.Image], Optional[Image.Image], Optional[Image.Image]]:
        """Generate random graph resources"""
        index = helper.rand_index(len(self.resources.rang_graph_image))
        if index < 0:
            return None, None, None
        
        graph_image = self.resources.rang_graph_image[index]
        return graph_image.overlay_image, graph_image.shadow_image, graph_image.mask_image
    
    def _gen_master_image(self, size: option.Size, shadow_image: Image.Image,
                         blocks: List[Block]) -> Tuple[Image.Image, Image.Image]:
        """Generate the main image and its prepared background"""
        draw_blocks = []
        for block in blocks:
            draw_block = DrawBlock()
            draw_block.block = block
            draw_block.x = block.x
            draw_block.y = block.y
            draw_block.width = block.width
            draw_block.height = block.height
            draw_block.angle = block.angle
            draw_block.image = shadow_image
            draw_blocks.append(draw_block)
        
        bg_image = randgen.rand_image(self.resources.rang_backgrounds)
        if bg_image:
            prepared_bg_image = helper.random_crop_resize(bg_image, size.width, size.height)
        else:
            prepared_bg_image = Image.new("RGBA", (size.width, size.height), (255, 255, 255, 255))

        master_image = self.draw_image.draw_with_nrgba(
            width=size.width,
            height=size.height,
            background=prepared_bg_image,
            alpha=self.opts.image_alpha,
            draw_blocks=draw_blocks
        )

        return master_image, prepared_bg_image.copy()
    
    def _gen_tile_image(self, mask_image: Image.Image, bg_image: Image.Image,
                       overlay_image: Image.Image, block: Block) -> Image.Image:
        """Generate the puzzle tile image"""
        draw_block = DrawBlock()
        draw_block.block = block
        draw_block.x = block.x
        draw_block.y = block.y
        draw_block.width = block.width
        draw_block.height = block.height
        draw_block.angle = block.angle
        draw_block.image = overlay_image
        
        return self.draw_image.draw_with_template(
            background=bg_image,
            mask_image=mask_image,
            alpha=self.opts.image_alpha,
            width=block.width,
            height=block.height,
            draw_block=draw_block
        )
    
    def _gen_graph_blocks(self, image_size: option.Size, size: option.RangeVal,
                         length: int) -> Tuple[List[Block], option.Point]:
        """Generate graph block data"""
        blocks = []
        width = image_size.width
        height = image_size.height
        
        rand_angle = self._rand_graph_angle()
        rand_size = base_random.rand_int(size.min, size.max)
        c_height = rand_size
        c_width = rand_size
        
        dzd_type = self._rand_dead_zone_direction()
        dp = c_width // 2
        block_width = (width - c_width - 20) // length
        y = self._calc_y_with_dead_zone(5, height - c_height - 5, c_height, dzd_type)
        
        for i in range(length):
            block = Block()
            start, end = self._calc_x_with_dead_zone(
                (i * block_width) + dp + 5,
                ((i + 1) * block_width) - dp,
                c_width,
                dzd_type
            )
            
            start = int(max(start, dp + 5))
            block.x = base_random.rand_int(start + 20, end + 20) - dp
            
            if self.opts.enable_graph_vertical_random:
                y = self._calc_y_with_dead_zone(5, height - c_height - 5, c_height, dzd_type)
            
            block.y = y
            block.width = c_width
            block.height = c_height
            block.angle = rand_angle
            
            blocks.append(block)
        
        point = option.Point(x=0, y=0)
        if self.mode == Mode.BASIC:
            point.x = base_random.rand_int(5, dp)
            point.y = y
            return blocks, point
        
        if dzd_type == DeadZoneDirectionType.TOP:
            point.x = base_random.rand_int(5, width - c_width - 5)
            point.y = 5
        elif dzd_type == DeadZoneDirectionType.BOTTOM:
            point.x = base_random.rand_int(5, width - c_width - 5)
            point.y = height - c_height - 5
        elif dzd_type == DeadZoneDirectionType.LEFT:
            point.x = 5
            point.y = base_random.rand_int(5, height - c_height - 5)
        elif dzd_type == DeadZoneDirectionType.RIGHT:
            point.x = width - c_width - 5
            point.y = base_random.rand_int(5, height - c_height - 5)
        
        return blocks, point
    
    def _calc_x_with_dead_zone(self, start: int, end: int, value: int,
                              dzd_type: int) -> Tuple[int, int]:
        """Calculate the X range with dead-zone handling"""
        if dzd_type == DeadZoneDirectionType.LEFT:
            start += value
            end += value
        return start, end
    
    def _calc_y_with_dead_zone(self, start: int, end: int, value: int, dzd_type: int) -> int:
        """Calculate Y with dead-zone handling"""
        if dzd_type == DeadZoneDirectionType.TOP:
            start += value
        elif dzd_type == DeadZoneDirectionType.BOTTOM:
            end -= value
        return base_random.rand_int(start, end)
    
    def _rand_dead_zone_direction(self) -> int:
        """Generate a random dead-zone direction"""
        dirs = self.opts.range_dead_zone_directions
        index = helper.rand_index(len(dirs))
        if index < 0:
            return 0
        return dirs[index]
    
    def _rand_graph_angle(self) -> int:
        """Generate a random graph angle"""
        angles = self.opts.range_graph_angle_pos
        index = helper.rand_index(len(angles))
        if index < 0:
            return 0
        
        angle = angles[index]
        return base_random.rand_int(angle.min, angle.max)

