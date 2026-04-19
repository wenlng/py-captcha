"""
pi-captcha package.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

__version__ = "0.0.1"

from pi_captcha.click import ClickBuilder
from pi_captcha.slide import SlideBuilder
from pi_captcha.slide_region import SlideRegionBuilder
from pi_captcha.rotate import RotateBuilder

from pi_captcha import click
from pi_captcha import slide
from pi_captcha import slide_region
from pi_captcha import rotate

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
