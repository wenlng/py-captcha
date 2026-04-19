"""
SlideRegion module exposing drag captcha aliases.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

from py_captcha.slide import SlideBuilder, validate
from py_captcha.slide.slide import SlideCaptcha

SlideRegionBuilder = SlideBuilder
SlideRegionCaptcha = SlideCaptcha


def new_slide_region_builder(*opts):
    """Create and return a SlideRegion builder."""
    return SlideBuilder(*opts)


__all__ = ["SlideRegionBuilder", "SlideRegionCaptcha", "new_slide_region_builder", "validate"]
