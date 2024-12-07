from functools import reduce
from typing import overload, Iterable, Self

from problem_instance_abc import ProblemInstanceABC
from util.vectors import pos, pos_range


def assert_equal_length(first: str, second: str) -> str:
    assert len(first) == len(second)
    return second


class RoomMap(tuple[str]):
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

        raise ValueError("InitialRoomMap.position(x): x not in map")

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
        return f"InitialRoomMap<{self.height} x {self.width}>"


class ProblemInstance(ProblemInstanceABC):
    initial_room_map: RoomMap
    obstructions: frozenset[pos]
    initial_guard_position: pos

    def parse_plaintext(self) -> None:
        lines = self.input_plaintext.splitlines()
        self.initial_room_map = RoomMap(lines)

        obstructions, guard_pos = self._find_points_of_interest()
        self.obstructions = frozenset(obstructions)
        self.initial_guard_position: pos = guard_pos

    def _find_points_of_interest(self) -> tuple[set[pos], pos]:
        """
        :return: a tuple of (obstructions, guard position)
        """
        obstructions: set[pos] = set()
        guard_pos: pos | None = None

        for room_pos in pos_range(self.initial_room_map.shape):
            character = self.initial_room_map[room_pos]
            if character == ".":
                continue
            if character == "#":
                obstructions.add(room_pos)
                continue
            if character == "^":
                assert guard_pos is None
                guard_pos = room_pos
                continue

        assert guard_pos is not None
        return obstructions, guard_pos
