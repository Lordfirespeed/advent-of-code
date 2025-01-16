from typing import (
    Iterable,
    Literal,
    SupportsBytes,
    SupportsIndex,
    SupportsInt,
    overload,
)

from numpy import integer


type BytesLike = Iterable[SupportsIndex] | SupportsBytes


def byte_length(value: SupportsInt) -> int:
    value = int(value)
    assert value > 0
    # 2^3 = 8, so right-shifting 3 times is equivalent to dividing by 8
    return ((value.bit_length() - 1) >> 3) + 1


def signed_byte_length(value: SupportsInt) -> int:
    value = int(value)
    # 2^3 = 8, so right-shifting 3 times is equivalent to dividing by 8
    return (value.bit_length() >> 3) + 1


def signed_bin(value: SupportsInt) -> str:
    value = int(value)
    binary_byte_length = signed_byte_length(value)
    binary_bit_length = binary_byte_length * 8
    signed_value_bytes = value.to_bytes(length=binary_byte_length, signed=True)
    unsigned_value_integer = int.from_bytes(signed_value_bytes)
    return f"{unsigned_value_integer:0{binary_bit_length}b}"


def last_set_bit_index(binary: SupportsInt | BytesLike) -> int | Literal[-1]:
    """
    Compute the index (from the right) of the right-most '1' bit in 'binary'.
    For integer powers of 2, this computes log_2(binary).
    If there exists no index (because the input contains no set bits), returns -1.
    """
    if isinstance(binary, SupportsInt):
        binary = int(binary)
    if type(binary) is not int:
        binary = int.from_bytes(binary, byteorder="big")

    if binary == 0:
        return -1

    # bit-hack to create a bit-mask of exactly 1 '1' bit, in the position of the right-most '1' bit from 'binary'
    highest_bit_mask = binary & -binary

    return highest_bit_mask.bit_length() - 1


def first_set_bit_index(binary: SupportsInt | BytesLike) -> int | Literal[-1]:
    """
    Compute the index (from the right) of the left-most '1' bit in 'binary'.
    If there exists no index (because the input contains no set bits), returns -1.
    """
    if isinstance(binary, SupportsInt):
        binary = int(binary)
    if type(binary) is not int:
        binary = int.from_bytes(binary, byteorder="big")
    
    if binary == 0:
        return -1
    
    return binary.bit_length() - 1


@overload
def circular_left_shift(value: integer, shift: int | integer, width: int | integer) -> integer: ...
@overload
def circular_left_shift(value: int, shift: int | integer, width: int | integer) -> int: ...

def circular_left_shift(value, shift, width):
    if isinstance(value, integer):
        return (value << shift) | (value >> (width - shift))
    # https://stackoverflow.com/a/63767548/11045433
    return ((value << shift) % (1 << width)) | (value >> (width - shift))

@overload
def circular_right_shift(value: integer, shift: int | integer, width: int | integer) -> integer: ...
@overload
def circular_right_shift(value: int, shift: int | integer, width: int | integer) -> int: ...

def circular_right_shift(value, shift, width):
    if isinstance(value, integer):
        return (value >> shift) | (value << (width - shift))
    return (value >> shift) | ((value << (width - shift)) % (1 << width))
