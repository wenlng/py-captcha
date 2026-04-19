"""
Slide captcha validation

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""


def validate(src_x: int, src_y: int, dx: int, dy: int, padding: int) -> bool:
    """
    Check whether a point falls within the allowed range
    
    Args:
        src_x: User interaction X coordinate
        src_y: User interaction Y coordinate
        dx: Target X coordinate
        dy: Target Y coordinate
        padding: Allowed tolerance
    
    Returns:
        Whether the point is within range
    """
    new_x = padding * 2
    new_y = padding * 2
    new_dx = dx - padding
    new_dy = dy - padding
    
    return (src_x >= new_dx and
            src_x <= new_dx + new_x and
            src_y >= new_dy and
            src_y <= new_dy + new_y)

