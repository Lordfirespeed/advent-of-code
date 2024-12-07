from typing import Generator, Iterable
from itertools import chain

from util.vectors import Position, pos

from .problem import ProblemInstance


class PartOneSolver:
    part_number_sum: int
    positions_to_check: Iterable[Position]
    partial_digit: str

    adjacencies: list[Position] = [
        pos(1, 0),
        pos(1, 1),
        pos(0, 1),
        pos(-1, 1),
        pos(-1, 0),
        pos(-1, -1),
        pos(0, -1),
        pos(1, -1),
    ]

    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance
        self.reset()

    def reset(self):
        self.part_number_sum = 0
        self.positions_to_check = []
        self.partial_digit = ""

    def is_in_bounds(self, position: Position) -> bool:
        return 0 <= position[0] < self.instance.schematic.height and 0 <= position[1] < self.instance.schematic.width

    def adjacent_positions(self, position: Position) -> Generator[Position]:
        for adjacency in self.adjacencies:
            adjacent_position = position + adjacency
            if not self.is_in_bounds(adjacent_position):
                continue
            yield adjacent_position

    def has_symbol(self, position: Position) -> bool:
        if self.instance.schematic[position] == ".": return False
        if self.instance.schematic[position].isdigit(): return False
        return True

    def pop_partial_digit(self) -> None:
        if self.partial_digit == "":
            return

        if any(self.has_symbol(position) for position in self.positions_to_check):
            self.part_number_sum += int(self.partial_digit)

        self.positions_to_check = []
        self.partial_digit = ""

    def consider_row(self, row_index: int) -> None:
        for column_index in range(self.instance.schematic.width):
            position = pos(row_index, column_index)
            if not self.instance.schematic[position].isdigit():
                self.pop_partial_digit()
                continue
            
            self.positions_to_check = chain(self.positions_to_check, self.adjacent_positions(position))
            self.partial_digit += self.instance.schematic[position]

    def solve(self) -> int:
        self.reset()
        for row_index in range(self.instance.schematic.height):
            self.consider_row(row_index)
        return self.part_number_sum
