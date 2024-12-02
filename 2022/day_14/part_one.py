from common.vectors import Vector2
from collections import defaultdict
from enum import Enum, auto
from typing import overload, Any
from copy import copy


class TileState(Enum):
    Air = auto()
    Rock = auto()
    Sand = auto()


class SandInVoid(Exception):
    pass


class Cave:
    def __init__(self, wall_strings: [str]) -> None:
        self.tiles: defaultdict[int, dict[int, TileState]] = defaultdict(dict)
        self.generate_walls(wall_strings)
        self.maximum_height_wall = max(self.tiles.keys())

    @staticmethod
    def line_of_vectors(start: Vector2, end: Vector2) -> [Vector2]:
        if start.x == end.x:
            if start.y > end.y:
                start, end = end, start

            return [Vector2(start.x, y) for y in range(start.y, end.y + 1)]

        if start.y == end.y:
            if start.x > end.x:
                start, end = end, start

            return [Vector2(x, start.y) for x in range(start.x, end.x + 1)]

        raise ValueError

    def generate_one_wall_segment(self, start: Vector2, end: Vector2) -> None:
        for position in self.line_of_vectors(start, end):
            self[position] = TileState.Rock

    def generate_one_wall(self, wall_string: str) -> None:
        string_vertex_positions = [vertex.split(",") for vertex in wall_string.split(" -> ")]
        vector_vertex_positions = [Vector2(int(x), int(y)) for x, y in string_vertex_positions]
        for vector_pair in zip(vector_vertex_positions[:-1], vector_vertex_positions[1:]):
            self.generate_one_wall_segment(*vector_pair)

    def generate_walls(self, wall_strings: [str]) -> None:
        for wall_string in wall_strings:
            self.generate_one_wall(wall_string)

    @overload
    def __getitem__(self, item: tuple[int, int] | Vector2) -> TileState: ...

    def __getitem__(self, item):
        try:
            if isinstance(item, Vector2):
                return self.tiles[item.y][item.x]

            if isinstance(item, tuple):
                assert len(item) == 2
                return self.tiles[item[1]][item[0]]
        except KeyError:
            return TileState.Air

        raise TypeError

    @overload
    def __setitem__(self, item: tuple[int, int] | Vector2, value: Any) -> None: ...

    def __setitem__(self, item, value):
        if isinstance(item, Vector2):
            self.tiles[item.y][item.x] = value
            return

        if isinstance(item, tuple):
            assert len(item) == 2
            self.tiles[item[1]][item[0]] = value
            return

        raise TypeError


class Solution:
    cave_class = Cave
    sand_source = Vector2(500, 0)
    sand_fall_deltas = (Vector2(0, 1), Vector2(-1, 1), Vector2(1, 1))
    void_offset = 0

    def __init__(self, input_lines: [str]) -> None:
        self.cave = self.cave_class(input_lines)
        self.number_sand_at_rest = 0
        self.void_from_y = self.cave.maximum_height_wall + self.void_offset

    def spawn_sand(self) -> None:
        current_sand_position = copy(self.sand_source)
        previous_sand_position = None
        while previous_sand_position != current_sand_position:
            previous_sand_position = current_sand_position
            for fall_delta in self.sand_fall_deltas:
                fall_to_position = current_sand_position + fall_delta
                if self.cave[fall_to_position] != TileState.Air:
                    continue
                current_sand_position = fall_to_position
                break
            else:
                break
            if current_sand_position.y > self.void_from_y:
                raise SandInVoid
        self.number_sand_at_rest += 1
        self.cave[current_sand_position] = TileState.Sand

    def run_simulation(self):
        while True:
            try:
                self.spawn_sand()
            except SandInVoid:
                break


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        input_lines = [line.strip() for line in input_file.readlines()]

    solver = Solution(input_lines)
    solver.run_simulation()
    result = solver.number_sand_at_rest
    print(f"Number of sand at rest: {result}")
