"""
Validation helpers for click captcha interactions.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""


def validate(src_x: int, src_y: int, dx: int, dy: int, width: int, height: int, padding: int) -> bool:
    """Return whether a click point falls within the target area plus tolerance."""
    new_width = width + (padding * 2)
    new_height = height + (padding * 2)
    new_dx = int(max(dx, dx - padding))
    new_dy = int(max(dy, dy - padding))

    return (
        src_x >= new_dx
        and src_x <= new_dx + new_width
        and src_y >= new_dy
        and src_y <= new_dy + new_height
    )
