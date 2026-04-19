"""
py-captcha package.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

__version__ = "0.0.1"

from py_captcha.click import ClickBuilder
from py_captcha.slide import SlideBuilder
from py_captcha.slide_region import SlideRegionBuilder
from py_captcha.rotate import RotateBuilder

from py_captcha import click
from py_captcha import slide
from py_captcha import slide_region
from py_captcha import rotate

__all__ = [
    "ClickBuilder",
    "SlideBuilder",
    "SlideRegionBuilder",
    "RotateBuilder",
    "click",
    "slide",
    "slide_region",
    "rotate",
]
