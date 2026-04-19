"""
Thread-local random generator helpers.

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""

import random
import secrets
import threading


_thread_local = threading.local()


def get_thread_random() -> random.Random:
    """Return a per-thread random generator instance."""
    if not hasattr(_thread_local, "rng"):
        seed = secrets.randbits(64)
        _thread_local.rng = random.Random(seed)
    return _thread_local.rng
