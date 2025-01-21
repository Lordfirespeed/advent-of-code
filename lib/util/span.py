from operator import index
from typing import (
    Iterator,
    Self,
    Sequence,
    SupportsIndex,
    overload,
)


class span(Sequence[int]):
    __slots__ = ("__start", "__stop")
    __start: int
    __stop: int

    @property
    def start(self) -> int:
        return self.__start

    @property
    def stop(self) -> int:
        return self.__stop

    @overload
    def __new__(cls, __stop: int) -> Self: ...

    @overload
    def __new__(cls, __start: int, __stop: int) -> Self: ...

    def __new__(cls, *args, **kwargs):
        if len(kwargs) > 0:
            raise TypeError(f"span() takes no keyword arguments")
        if len(args) == 0:
            raise TypeError("span() expected at least 1 argument, got 0")
        if len(args) == 1:
            return cls(0, *args)
        if len(args) > 2:
            raise TypeError(f"span() expected at most 2 arguments, got {len(args)}")

        __start, __stop = args
        if not isinstance(__start, SupportsIndex):
            raise TypeError(f"{__start.__class__.__name__} object cannot be interpreted as an index")
        if not isinstance(__stop, SupportsIndex):
            raise TypeError(f"{__stop.__class__.__name__} object cannot be interpreted as an index")

        new_object = super().__new__(cls)
        new_object.__start = index(__start)
        new_object.__stop = index(__stop)
        return new_object

    def count(self, __value: object) -> int:
        if __value in self:
            return 1
        return 0

    @overload
    def index(self, __value: int) -> int: ...

    @overload
    def index(self, __value: Self) -> slice: ...

    def index(self, __value):
        if isinstance(__value, int):
            return self.__index_of_int(__value)

        if isinstance(__value, span):
            return self.__index_of_span(__value)

        raise TypeError("can only search for objects of type int, span in span")

    def __index_of_int(self, __value: int) -> int:
        if not isinstance(__value, int):
            raise TypeError(f"{__value.__class__.__name__} object cannot be interpreted as an int")

        if __value < self.start or self.__stop <= __value:
            raise ValueError(f"{__value} is not in span")
        return __value - self.__start

    def __index_of_span(self, __value: Self) -> slice:
        if __value.start < self.start or __value.stop > self.stop:
            raise ValueError(f"{__value} is not enclosed by span")

        return slice(__value.start - self.start, __value.stop - self.start)

    def __len__(self) -> int:
        return max(0, self.stop - self.start)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, span):
            return False

        if self.start != __value.start:
            return False

        return len(self) == len(__value)

    def __hash__(self) -> int:
        raise TypeError("unhashable type: 'span'")

    def __contains__(self, __value: object) -> bool:
        if not isinstance(__value, int):
            return False

        return self.start <= __value < self.__stop

    def __iter__(self) -> Iterator[int]:
        return iter(range(self.__start, self.__stop))

    def __reversed__(self):
        return reversed(range(self.__stop, self.__start, -1))

    @overload
    def __getitem__(self, __key: SupportsIndex) -> int: ...

    @overload
    def __getitem__(self, __key: slice) -> Self: ...

    def __getitem__(self, __key):
        if isinstance(__key, int):
            return self.__get_int_item(__key)

        if isinstance(__key, SupportsIndex):
            return self[index(__key)]

        if isinstance(__key, slice):
            return self.__get_slice_item(__key)

        raise TypeError(f"span indices must be integers or slices, not {__key.__class__.__name__}")

    def __get_int_item(self, __key: int) -> int:
        self_length = len(self)
        if __key < 0:
            negative_index = self_length + __key
            if negative_index < 0:
                raise IndexError("span index out of range")
            return self.__get_int_item(negative_index)
        if __key >= self_length:
            raise IndexError("span index out of range")

        return self.__start + __key

    def __get_slice_item(self, __key: slice) -> Self:
        if __key.step is not None:
            raise TypeError("span can only be indexed by slice with step None")
        start, stop, step = __key.indices(len(self))

        return self.__class__(self.start + start, min(self.start + stop, self.stop))

    def __repr__(self) -> str:
        return f"span({self.start}, {self.stop})"

    @classmethod
    def _ordered_intersection(cls, first: Self, second: Self) -> Self:
        endpoint = min(first.stop, second.stop)
        return cls(second.start, endpoint)

    def intersection(self, other: Self) -> Self:
        if self.start <= other.start:
            return self._ordered_intersection(self, other)
        return self._ordered_intersection(other, self)

    @classmethod
    def _ordered_difference(cls, first: Self, second: Self) -> tuple[Self, Self]:
        first_span = cls(first.start, second.start)
        second_span = cls(second.stop, first.stop)
        return first_span, second_span

    def difference(self, other: Self) -> tuple[Self, Self]:
        first_span = self.__class__(self.start, other.start)
        second_span = self.__class__(other.stop, self.stop)
        return first_span, second_span

    def union(self, other: Self) -> Self:
        if self.stop < other.start:
            raise ValueError
        if other.stop < self.start:
            raise ValueError

        return self.__class__(
            min(self.start, other.start),
            max(self.stop, other.stop),
        )
