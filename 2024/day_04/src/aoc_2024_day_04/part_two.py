from typing import ClassVar, Iterable

from util.vectors import pos, pos_range

from .problem import ProblemInstance


class PartTwoSolver:
    target_count: int

    target: ClassVar[str] = "MAS"
    search_directions: ClassVar[list[pos]] = [
        pos(-1, 1),
        pos(1, 1),
    ]

    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance
        self.reset()

    def reset(self):
        self.target_count = 0

    def is_in_bounds(self, position: pos) -> bool:
        if not (0 <= position[0] < self.instance.word_search.height):
            return False
        if not (0 <= position[1] < self.instance.word_search.width):
            return False
        return True

    def characters_along(self, positions: Iterable[pos]) -> Iterable[str]:
        return (self.instance.word_search[position] for position in positions)

    def word_along(self, positions: Iterable[pos]) -> str:
        return "".join(self.characters_along(positions))

    def search_from_in_direction(self, position: pos, direction: pos) -> bool:
        positions = (position - direction, position, position + direction)
        if not self.is_in_bounds(positions[0]):
            return False
        if not self.is_in_bounds(positions[-1]):
            return False

        word = self.word_along(positions)
        return word == self.target or word == self.target[::-1]

    def search_from(self, position: pos) -> None:
        if not all(self.search_from_in_direction(position, direction) for direction in self.search_directions):
            return

        self.target_count += 1

    def solve(self) -> int:
        for position in pos_range(self.instance.word_search.shape):
            self.search_from(position)

        return self.target_count
