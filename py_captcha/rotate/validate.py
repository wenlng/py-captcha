"""
Rotate captcha validation

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""


def validate(angle: int, d_angle: int, padding: int) -> bool:
    """
    Check whether a rotation angle falls within the allowed range
    
    Args:
        angle: Current angle
        d_angle: Target angle
        padding: Allowed angle tolerance
    
    Returns:
        Whether the angle is within range
    """
    min_angle = 360 - padding
    max_angle = 360 + padding
    angle += d_angle
    
    return angle >= min_angle and angle <= max_angle

