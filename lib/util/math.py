from math import (
    isqrt as isqrt_floor,
    prod as product,
    sumprod as sum_product,
)

__all__ = (
    "isqrt_floor",
    "isqrt_ceil",
    "floor_div",
    "ceil_div",
    "product",
    "sum_product",
)


def isqrt_ceil(n: int) -> int:
    """
    https://docs.python.org/3/library/math.html#math.isqrt
    """
    return 1 + isqrt_floor(n - 1)


def floor_div(a, b):
    return a // b


def ceil_div(a, b):
    """https://stackoverflow.com/a/17511341/11045433"""
    return -(a // -b)
