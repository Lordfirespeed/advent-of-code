from math import prod, sumprod


def floor_div(a,b):
    return a // b


def ceil_div(a, b):
    """https://stackoverflow.com/a/17511341/11045433"""
    return -(a // -b)
