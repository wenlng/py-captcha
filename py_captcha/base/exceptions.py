"""
Custom exception types used by py-captcha.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com
"""


class CaptchaError(Exception):
    """Base exception for captcha-related errors."""


class CaptchaConfigError(CaptchaError):
    """Raised when captcha configuration is invalid."""


class CaptchaResourceError(CaptchaError):
    """Raised when required captcha resources are missing or invalid."""


class CaptchaGenerationError(CaptchaError):
    """Raised when captcha generation fails."""


class CaptchaValidationError(CaptchaError):
    """Raised when captcha validation fails."""
