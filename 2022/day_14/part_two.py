from common.vectors import Vector2
from part_one import TileState, Cave, Solution


class CaveWithFloor(Cave):
    def __getitem__(self, item):
        try:
            if isinstance(item, Vector2):
                if item.y >= self.maximum_height_wall + 2:
                    return TileState.Rock
                return self.tiles[item.y][item.x]

            if isinstance(item, tuple):
                assert len(item) == 2
                if item[1] >= self.maximum_height_wall + 2:
                    return TileState.Rock
                return self.tiles[item[1]][item[0]]
        except KeyError:
            return TileState.Air

        raise TypeError


class PartTwoSolution(Solution):
    cave_class = CaveWithFloor
    void_offset = 2

    def run_simulation(self):
        while self.cave[self.sand_source] != TileState.Sand:
            self.spawn_sand()


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        input_lines = [line.strip() for line in input_file.readlines()]

    solver = PartTwoSolution(input_lines)
    solver.run_simulation()
    result = solver.number_sand_at_rest
    print(f"Number of sand at rest: {result}")
