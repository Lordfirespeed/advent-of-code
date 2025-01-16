from operator import index
from typing import (
    ClassVar,
    Iterator,
    Literal, 
    Self, 
    Sequence,
    SupportsIndex, 
    TypeGuard, 
    final, 
    overload, 
)

import numpy as np
import numpy.linalg

from .classproperty import classproperty
from .math import ceil_div, prod


_vector2 = np.ndarray[tuple[Literal[2]], np.dtype[object]]
_matrix2by2 = np.ndarray[tuple[Literal[2], Literal[2]], np.dtype[object]]


class pos(_vector2, metaclass=classproperty.Meta):
    anticlockwise_rotation_matrix: ClassVar[_matrix2by2] = np.array([[0, -1], [1, 0]])
    clockwise_rotation_matrix: ClassVar[_matrix2by2] = -anticlockwise_rotation_matrix
    anticlockwise_rotation_matrix.setflags(write=False)
    clockwise_rotation_matrix.setflags(write=False)

    @classmethod
    def immutable(cls, y: int, x: int) -> Self:
        instance = cls(y, x)
        instance.setflags(write=False)
        return instance

    @classmethod
    def mutable(cls, y: int, x: int) -> Self:
        instance = cls(y, x)
        instance.setflags(write=True)
        return instance

    def as_immutable(self) -> Self:
        return self.__class__.immutable(*self)
    
    def as_mutable(self) -> Self:
        return self.__class__.mutable(*self)

    @classproperty
    @classmethod
    def zero(cls: Self):
        return cls.immutable(0, 0)

    def rotate_clockwise(self, *, repeat=1) -> Self:
        repeat %= 4
        repeated_rotation_matrix = numpy.linalg.matrix_power(self.clockwise_rotation_matrix, repeat)
        return repeated_rotation_matrix @ self

    def rotate_anticlockwise(self, *, repeat=1) -> Self:
        repeat %= 4
        repeated_rotation_matrix = numpy.linalg.matrix_power(self.anticlockwise_rotation_matrix, repeat)
        return repeated_rotation_matrix @ self

    @overload
    def __getitem__(self, item: Literal[0, 1]) -> int: ...
    
    @overload
    def __getitem__(self, item: tuple[Literal[0,1]]) -> int: ...

    def __getitem__(self, item):
        if isinstance(item, tuple):
            if len(item) != 1:
                raise IndexError(f"too many indices for pos: pos is 1-dimensional, but {len(item)} were indexed")
            return self[item[0]]
        if not isinstance(item, SupportsIndex):
            raise TypeError("pos indices must be integers or None or have an __index__ method")
        return super().__getitem__(item)

    def __new__(cls, y: int, x: int):
        assert isinstance(y, int)
        assert isinstance(x, int)
        buffer = np.array((y, x), dtype=object)
        new_object = super().__new__(cls, (2,), buffer=buffer, dtype=object)
        new_object.setflags(write=False)
        return new_object

    def __eq__(self, other) -> bool:
        if not isinstance(other, pos):
            return super().__eq__(other)
        return np.array_equal(self, other)

    def __hash__(self) -> int:
        return hash((self[0], self[1]))

    def __ge__(self, other) -> np.ndarray[tuple[Literal[2]], np.dtype[bool]]:
        return np.greater_equal(self, other, out=np.ndarray((2,), dtype=bool), casting="unsafe")

    def __le__(self, other) -> np.ndarray[tuple[Literal[2]], np.dtype[bool]]:
        return np.less_equal(self, other, out=np.ndarray((2,), dtype=bool), casting="unsafe")

    def __gt__(self, other) -> np.ndarray[tuple[Literal[2]], np.dtype[bool]]:
        return np.greater(self, other, out=np.ndarray((2,), dtype=bool), casting="unsafe")

    def __lt__(self, other) -> np.ndarray[tuple[Literal[2]], np.dtype[bool]]:
        return np.less(self, other, out=np.ndarray((2,), dtype=bool), casting="unsafe")

    def __repr__(self):
        return f"pos({self[0]}, {self[1]})"


type Position = pos


def is_pos(value: object) -> TypeGuard[Position]:
    return isinstance(value, pos)


@final
class pos_range(Sequence[Position]):
    __slots__ = ("__start", "__stop", "__step")
    __start: Position
    __stop: Position
    __step: int

    @property
    def start(self) -> Position:
        return self.__start

    @property
    def stop(self) -> Position:
        return self.__stop

    @property
    def step(self):
        return self.__step

    @overload
    def __new__(cls, __stop: Position) -> Self: ...

    @overload
    def __new__(cls, __start: Position, __stop: Position, __step: int = ...) -> Self: ...

    def __new__(cls, *args, **kwargs):
        if len(kwargs) > 0:
            raise TypeError(f"pos_range() takes no keyword arguments")
        if len(args) == 0:
            raise TypeError("pos_range() expected at least 1 argument, got 0")
        if len(args) == 1:
            return pos_range(pos(0, 0), *args)
        if len(args) == 2:
            return pos_range(*args, 1)
        if len(args) > 3:
            raise TypeError(f"pos_range() expected at most 3 arguments, got {len(args)}")

        __start, __stop, __step = args
        if not is_pos(__start):
            raise TypeError(f"{__start.__class__.__name__} object cannot be interpreted as a position")
        if not is_pos(__stop):
            raise TypeError(f"{__stop.__class__.__name__} object cannot be interpreted as a position")
        if not isinstance(__step, SupportsIndex):
            raise TypeError(f"{__step.__class__.__name__} object cannot be interpreted as an integer")

        new_object = super().__new__(cls)
        new_object.__start = __start
        new_object.__stop = __stop
        new_object.__step = index(__step)
        return new_object

    def count(self, __value: object) -> int:
        if __value in self:
            return 1
        return 0

    def index(self, __value: object) -> int:  # type: ignore[override]
        if not is_pos(__value):
            raise TypeError(f"{__value.__class__.__name__} object cannot be interpreted as a position")

        step_total = 0
        for dimension in range(2):
            length_in_dimension = self.__length_in_dimension(dimension)
            step_total *= length_in_dimension

            steps, difference = divmod(__value[dimension] - self.start[dimension], self.step)
            if difference != 0 or steps < 0 or steps >= length_in_dimension:
                raise ValueError(f"{__value} is not in pos_range")

            step_total += steps
        return step_total

    def __length_in_dimension(self, d: int):
        return max(0, ceil_div(self.stop[d] - self.start[d], self.step))

    def shape(self) -> tuple[int, ...]:
        return tuple(self.__length_in_dimension(d) for d in range(2))

    def __len__(self) -> int:
        return prod(self.shape())

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, pos_range):
            return False

        if self.step != __value.step:
            return False

        if (self.start != __value.start).any():
            return False

        return self.shape() == __value.shape()

    def __hash__(self) -> int:
        raise TypeError("unhashable type: 'pos_range'")

    def __contains__(self, __value: object) -> bool:
        if not is_pos(__value):
            return False

        for dimension in range(2):
            steps, difference = divmod(__value[dimension] - self.start[dimension], self.step)
            if difference != 0 or steps < 0 or steps >= self.__length_in_dimension(dimension):
                return False
        return True

    def __iter__(self) -> Iterator[Position]:
        return pos_range_iterator(self.start, self.stop, self.step, self.shape())

    def __reversed__(self) -> Iterator[Position]:
        return pos_range_iterator(self.stop - self.step, self.start - self.step, -self.step, self.shape())

    @overload
    def __getitem__(self, __key: SupportsIndex) -> Position: ...

    @overload
    def __getitem__(self, __key: slice) -> Self: ...

    def __getitem__(self, __key):
        if isinstance(__key, int):
            return self.__get_int_item(__key)

        if isinstance(__key, SupportsIndex):
            return self[index(__key)]

        raise TypeError(f"pos_range indices must be integers, not {__key.__class__.__name__}")

    def __get_int_item(self, __key: int) -> Self:
        self_length = len(self)
        if __key < 0:
            negative_index = self_length + __key
            if negative_index < 0:
                raise IndexError("pos_range index out of range")
            return self.__get_int_item(negative_index)
        if __key >= self_length:
            raise IndexError("pos_range index out of range")

        dimension_sizes = np.ones((2,), dtype=object)
        for dimension in reversed(range(1, 2)):
            dimension_sizes[dimension - 1] = dimension_sizes[dimension] * self.__length_in_dimension(dimension)

        cursor = pos.zero
        for dimension in range(2):
            steps, difference = divmod(__key, dimension_sizes[dimension])
            cursor[dimension] = steps
            __key = difference

        return self.start + self.step * cursor

    def __repr__(self):
        if self.step == 1:
            return f"pos_range({repr(self.start)}, {repr(self.stop)})"
        return f"pos_range({repr(self.start)}, {repr(self.stop)}, {self.step})"


class pos_range_iterator(Iterator[Position]):
    __slots__ = ("start", "step", "shape", "cursor")
    start: Position
    step: int
    shape: tuple[int, ...]
    cursor: Position

    def __init__(self, start: Position, stop: Position, step: int, shape: tuple[int, ...]) -> None:
        self.start = start
        self.step = step
        self.shape = shape
        self.cursor = pos.zero.as_mutable()

    def __iter__(self) -> Iterator[Position]:
        return self

    def __next__(self) -> Position:
        if self.cursor[0] >= self.shape[0]:
            raise StopIteration

        value = self.start + self.step * self.cursor

        dimension = len(self.shape) - 1
        self.cursor[dimension] += 1
        while dimension > 0 and self.cursor[dimension] >= self.shape[dimension]:
            self.cursor[dimension] = 0
            dimension -= 1
            self.cursor[dimension] += 1

        return value
