from dataclasses import dataclass
from functools import reduce
from typing import overload

from problem_instance_abc import ProblemInstanceABC
from util.vectors import pos


def assert_equal_length(first: str, second: str) -> str:
    assert len(first) == len(second)
    return second


@dataclass
class Schematic(list[str]):
    def __init__(self, *args, **kwargs) -> None:
        if len(args) > 0:
            iterable = args[0]
            assert all(isinstance(value, str) for value in iterable)
        super().__init__(*args, **kwargs)
        reduce(assert_equal_length, self)
    
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

    @overload
    def __getitem__(self, item: pos) -> str: ...

    @overload
    def __getitem__(self, item: int) -> str: ...

    @overload
    def __getitem__(self, item: slice) -> list[str]: ...

    def __getitem__(self, item):
        if isinstance(item, pos):
            assert item.shape == (2,)
            y,x = item
            return super().__getitem__(y).__getitem__(x)
        return super().__getitem__(item)
    
    def __str__(self) -> str:
        return "\n".join(self)
    
    def __repr__(self) -> str:
        return f"Schematic<{self.height} x {self.width}>"


class ProblemInstance(ProblemInstanceABC):
    schematic: Schematic
    
    def parse_plaintext(self) -> None:
        lines = self.input_plaintext.splitlines()
        self.schematic = Schematic(lines)
