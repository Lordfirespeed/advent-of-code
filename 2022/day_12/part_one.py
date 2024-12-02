from dataclasses import dataclass, field
from string import ascii_lowercase
from typing import Self, overload, ClassVar
from common.vectors import Vector2


@dataclass(eq=False)
class MountainPeak:
    position: Vector2
    height: int

    @classmethod
    def from_symbol(cls, position: Vector2, symbol: str) -> Self:
        height = ascii_lowercase.index(symbol)
        return cls(position, height)

    def __eq__(self, other):
        if not isinstance(other, MountainPeak):
            raise TypeError
        return other.position == self.position

    def __repr__(self) -> str:
        return f"{ascii_lowercase[self.height]} at {self.position}"


class MountainRange:
    start_symbol = "S"
    end_symbol = "E"

    start_elevation = 0  # elevation "a"
    end_elevation = 25  # elevation "z"

    adjacencies = [
        Vector2(1, 0),
        Vector2(-1, 0),
        Vector2(0, 1),
        Vector2(0, -1)
    ]

    peak_class = MountainPeak

    def __init__(self, mountain_string: str) -> None:
        self.start_peak: MountainPeak = None
        self.end_peak: MountainPeak = None
        self.grid: [[MountainPeak]] = []
        self.fill_grid(mountain_string)

    @overload
    def __getitem__(self, key: Vector2 | tuple[int, int]) -> MountainPeak: ...

    @overload
    def __getitem__(self, key: int) -> [MountainPeak]: ...

    @overload
    def __getitem__(self, key: slice) -> [[MountainPeak]]: ...

    def __getitem__(self, key):
        if isinstance(key, Vector2):
            return self.grid[key.y][key.x]

        if isinstance(key, tuple):
            assert len(key) == 2
            return self.grid[key[1]][key[0]]

        if isinstance(key, int) or isinstance(key, slice):
            return self.grid[key]

        raise TypeError(f"Unsupported index type for {self.__class__.__name__}")

    def fill_grid(self, mountain_string: str):
        for y, line in enumerate(mountain_string.split("\n")):
            node_row = [self.make_peak(Vector2(x, y), character) for x, character in enumerate(line.strip())]
            self.grid.append(node_row)

    def make_peak(self, position: Vector2, character: str) -> MountainPeak:
        if character == self.start_symbol:
            node = self.peak_class(position, self.start_elevation)
            self.start_peak = node
            return node
        if character == self.end_symbol:
            node = self.peak_class(position, self.end_elevation)
            self.end_peak = node
            return node
        return self.peak_class.from_symbol(position, character)

    def adjacent_peaks(self, peak: MountainPeak) -> [MountainPeak]:
        assert self[peak.position] is peak
        adjacents = []
        for adjacency in self.adjacencies:
            getting_position = peak.position + adjacency
            try:
                assert getting_position.x >= 0
                assert getting_position.y >= 0
            except AssertionError:
                continue

            try:
                adjacent_peak = self[getting_position]
                adjacents.append(adjacent_peak)
            except IndexError:
                pass
        return adjacents

    def pathable_peaks(self, peak: MountainPeak) -> [MountainPeak]:
        return filter(lambda to_peak: self.is_pathable(peak, to_peak), self.adjacent_peaks(peak))

    @staticmethod
    def is_pathable(from_peak: MountainPeak, to_peak: MountainPeak) -> bool:
        height_difference = to_peak.height - from_peak.height
        return height_difference <= 1

    def calculate_distance_to_end(self, peak: MountainPeak) -> float:
        return abs(peak.position - self.end_peak.position)


@dataclass(eq=True, order=True)
class MountainNode:
    peak: MountainPeak = field(compare=False)
    parent: Self | None = field(default=None, compare=False)

    g_score: int | float = field(default=float("inf"), compare=False)  # weight to get from start to here
    h_score: float = field(default=float("inf"), compare=False)  # estimated weight to get from here to target

    f_score: float = field(default=float("inf"), compare=True)  # sum of the above weights

    def __repr__(self) -> str:
        return f"Node for {self.peak}"


class MountainPathfinder:
    weight_per_step: ClassVar[int] = 1

    def __init__(self, grid: MountainRange) -> None:
        self.grid: MountainRange = grid
        self.nodes_to_consider: [MountainNode] = []  # the "open" list
        self.nodes_already_considered: [MountainNode] = []  # the "closed" list

        self.start_node = MountainNode(self.grid.start_peak)
        self.start_node.g_score = 0
        self.nodes_to_consider.append(self.start_node)

    @staticmethod
    def find_node_of_peak(peak: MountainPeak, list_of_nodes: [MountainNode]) -> MountainNode:
        for node in list_of_nodes:
            if node.peak == peak:
                return node
        raise ValueError

    def find_peak_in_open_list(self, peak: MountainPeak) -> MountainNode:
        return self.find_node_of_peak(peak, self.nodes_to_consider)

    def find_peak_in_closed_list(self, peak: MountainPeak) -> MountainNode:
        return self.find_node_of_peak(peak, self.nodes_already_considered)

    def consider_node(self, node: MountainNode) -> None:
        adjacent_peaks = self.grid.pathable_peaks(node.peak)
        successors = map(MountainNode, adjacent_peaks)
        for successor in successors:
            successor.parent = node
            successor.g_score = node.g_score + self.weight_per_step
            successor.h_score = self.grid.calculate_distance_to_end(successor.peak)
            successor.f_score = successor.g_score + successor.h_score

            try:
                possibly_better_node = self.find_peak_in_open_list(successor.peak)
                if possibly_better_node.g_score <= node.g_score:
                    continue

                possibly_better_node.parent = node
                possibly_better_node.g_score = successor.g_score
                continue
            except ValueError:
                pass

            try:
                possibly_better_node = self.find_peak_in_closed_list(successor.peak)
                if possibly_better_node.g_score <= node.g_score:
                    continue

                possibly_better_node.parent = node  # potential error here; g-scores of children technically need to be updated
                continue
            except ValueError:
                pass

            self.nodes_to_consider.append(successor)

    def sort_best_nodes_first(self):
        self.nodes_to_consider.sort()

    def pathfinding_step(self):
        self.sort_best_nodes_first()
        best_node = self.nodes_to_consider.pop(0)
        self.consider_node(best_node)
        self.nodes_already_considered.append(best_node)

    def pathfind_until_first_solution(self):
        while True:
            try:
                self.end_node()
                break
            except ValueError:
                pass
            self.pathfinding_step()

    def pathfind_until_exhausted_solutions(self):
        while self.nodes_to_consider:
            self.pathfinding_step()

    def end_node(self):
        return self.find_peak_in_closed_list(self.grid.end_peak)

    def route(self):
        tail = self.end_node()
        route = [tail.peak]
        while tail.parent:
            tail = tail.parent
            route.insert(0, tail.peak)
        return route

    def fewest_steps_to_target(self):
        return len(self.route()) - 1


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        mountain_string = input_file.read()

    grid = MountainRange(mountain_string)
    solver = MountainPathfinder(grid)
    solver.pathfind_until_exhausted_solutions()
    result = solver.fewest_steps_to_target()
    print(f"Fewest steps to target: {result}")
