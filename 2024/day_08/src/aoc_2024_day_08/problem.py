from functools import reduce
from typing import overload, Iterable, Self

from problem_instance_abc import ProblemInstanceABC
from util.vectors import pos


def assert_equal_length(first: str, second: str) -> str:
    assert len(first) == len(second)
    return second


class AntennaMap(tuple[str]):
    def __new__(cls, __iterable: Iterable[str] = None) -> Self:
        if __iterable is None:
            return super().__new__(cls)

        assert all(isinstance(value, str) for value in __iterable)
        reduce(assert_equal_length, __iterable)
        return super().__new__(cls, __iterable)

    @property
    def width(self):
        if len(self) == 0:
            return 0
        return len(super().__getitem__(0))

    @property
    def height(self):
        return len(self)

    @property
    def shape(self):
        return pos(self.height, self.width)

    def position(self, item: object) -> pos:
        if not isinstance(item, str):
            raise TypeError
        if len(item) != 1:
            raise ValueError

        for y_index, row in enumerate(self):
            try:
                x_index = row.index(item)
                return pos(y_index, x_index)
            except ValueError:
                pass

        raise ValueError("AntennaMap.position(x): x not in map")

    @overload
    def __getitem__(self, item: pos) -> str: ...

    @overload
    def __getitem__(self, item: int) -> str: ...

    @overload
    def __getitem__(self, item: slice) -> list[str]: ...

    def __getitem__(self, item):
        if isinstance(item, pos):
            assert item.shape == (2,)
            y, x = item
            return super().__getitem__(y).__getitem__(x)
        return super().__getitem__(item)

    def __str__(self) -> str:
        return "\n".join(self)

    def __repr__(self) -> str:
        return f"AntennaMap<{self.height} x {self.width}>"


class ProblemInstance(ProblemInstanceABC):
    antenna_map: AntennaMap

    def parse_plaintext(self) -> None:
        lines = self.input_plaintext.splitlines()
        self.antenna_map = AntennaMap(lines)
