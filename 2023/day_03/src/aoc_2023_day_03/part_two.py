from typing import Generator

from util.vectors import Position, pos, pos_range

from .problem import ProblemInstance


class PartTwoSolver:
    gear_ratio_sum: int

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
        self.gear_ratio_sum = 0

    def is_in_bounds(self, position: Position) -> bool:
        return 0 <= position[0] < self.instance.schematic.height and 0 <= position[1] < self.instance.schematic.width

    def adjacent_positions(self, position: Position) -> Generator[Position]:
        for adjacency in self.adjacencies:
            adjacent_position = position + adjacency
            if not self.is_in_bounds(adjacent_position):
                continue
            yield adjacent_position

    def consider_asterisk(self, asterisk_position: Position) -> None:
        digit_neighbor_positions: set[Position] = {neighbor for neighbor in self.adjacent_positions(asterisk_position) if self.instance.schematic[neighbor].isdigit()}
        if len(digit_neighbor_positions) == 0:
            return

        def explore_digit_region(initial_position: Position) -> list[Position]:
            nonlocal digit_neighbor_positions
            region: list[Position] = [initial_position]

            while self.is_in_bounds(left_neighbor := region[0] + pos(0, -1)) and self.instance.schematic[left_neighbor].isdigit():
                digit_neighbor_positions.discard(left_neighbor)
                region.insert(0, left_neighbor)

            while self.is_in_bounds(right_neighbor := region[-1] + pos(0, 1)) and self.instance.schematic[right_neighbor].isdigit():
                digit_neighbor_positions.discard(right_neighbor)
                region.append(right_neighbor)

            return region

        digit_neighbor_regions: list[list[Position]] = []
        while digit_neighbor_positions:
            digit_region = explore_digit_region(digit_neighbor_positions.pop())
            digit_neighbor_regions.append(digit_region)

        if len(digit_neighbor_regions) != 2:
            return  # not a gear as should be adjacent to exactly 2 part numbers

        digit_strings = ["".join(self.instance.schematic[position] for position in region) for region in digit_neighbor_regions]
        first, second = (int(digit_string) for digit_string in digit_strings)
        self.gear_ratio_sum += first * second

    def solve(self) -> int:
        for check_position in pos_range(self.instance.schematic.shape):
            character = self.instance.schematic[check_position]
            if character != "*":
                continue
            self.consider_asterisk(check_position)

        return self.gear_ratio_sum
