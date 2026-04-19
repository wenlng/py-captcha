"""
Thread-safe random number helpers.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

import secrets
from typing import List

from pi_captcha.base.thread_random import get_thread_random


def rand_int(min_val: int, max_val: int) -> int:
    """Generate a secure random integer in the inclusive range [min_val, max_val]."""
    if min_val > max_val:
        return max_val

    if min_val == max_val:
        return min_val

    if min_val < 0:
        f64_min = abs(float(min_val))
        i64_min = int(f64_min)
        result = secrets.randbelow(max_val + 1 + i64_min)
        return result - i64_min

    result = secrets.randbelow(max_val - min_val + 1)
    return min_val + result


def perm(n: int) -> List[int]:
    """Return a shuffled permutation of integers from 0 to n - 1."""
    if n <= 0:
        return []
    if n == 1:
        return [0]

    rng = get_thread_random()
    result = list(range(n))
    rng.shuffle(result)
    return result
