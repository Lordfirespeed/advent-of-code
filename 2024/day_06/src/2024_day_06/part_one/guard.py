from dataclasses import dataclass, field
from typing import Container, Iterator

from util.vectors import pos


@dataclass(frozen=True)
class Guard:
    room_obstructions: Container[pos]
    room_shape: pos
    location: pos = field()
    facing: pos = field(default_factory=lambda: pos(-1, 0))

    def positions(self) -> Iterator[pos]:
        return _GuardPositionIterator(
            self.room_obstructions,
            self.room_shape,
            self.location.copy(),
            self.facing.copy(),
        )


@dataclass
class _GuardPositionIterator(Iterator[pos]):
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
        if not self.is_in_room_bounds():
            raise StopIteration
        previous_location = self.location.copy()
        if self.is_blocked():
            self.turn_right()
        self.step_forward()
        return previous_location
