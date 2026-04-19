"""
Block models for rotate captcha generation.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""


class Block:
    """Block metadata for rotate captcha results."""

    def __init__(self):
        self.parent_width = 0
        self.parent_height = 0
        self.width = 0
        self.height = 0
        self.angle = 0
