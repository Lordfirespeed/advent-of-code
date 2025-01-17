from dataclasses import dataclass, field
from typing import Container, Iterator

from util.vectors import pos


@dataclass
class _GuardTurnIterator(Iterator[pos]):
    room_obstructions: Container[pos]
    room_shape: pos
    location: pos = field()
    facing: pos = field(default_factory=lambda: pos(-1, 0))

    def __post_init__(self):
        self.location = self.location.as_mutable()

    def is_blocked(self) -> bool:
        return (self.location + self.facing) in self.room_obstructions

    def is_in_room_bounds(self) -> bool:
        return 0 <= self.location[0] < self.room_shape[0] and 0 <= self.location[1] < self.room_shape[1]

    def turn_right(self) -> None:
        self.facing = self.facing.rotate_clockwise()

    def step_forward(self) -> None:
        self.location += self.facing

    def __iter__(self) -> Iterator[pos]:
        return self

    def __next__(self) -> pos:
        while True:
            if not self.is_in_room_bounds():
                raise StopIteration
            if self.is_blocked():
                self.turn_right()
                return self.location.copy()

            self.step_forward()


@dataclass(frozen=True)
class Guard:
    room_obstructions: Container[pos]
    room_shape: pos
    location: pos = field()
    facing: pos = field(default_factory=lambda: pos(-1, 0))

    def _turn_positions(self) -> _GuardTurnIterator:
        return _GuardTurnIterator(
            self.room_obstructions,
            self.room_shape,
            self.location.copy(),
            self.facing.copy(),
        )

    def turn_positions(self) -> Iterator[pos]:
        return self._turn_positions()

    def detect_cycle(self) -> bool:
        one_speed = self._turn_positions()
        two_speed = self._turn_positions()

        def step() -> bool:
            nonlocal one_speed
            nonlocal two_speed

            next(one_speed)
            next(two_speed)
            next(two_speed)

            return one_speed.location == two_speed.location and one_speed.facing == two_speed.facing

        try:
            while True:
                if step():
                    return True
        except StopIteration:
            return False
