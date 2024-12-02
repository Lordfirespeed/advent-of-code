from dataclasses import dataclass, field
from typing import Self, ClassVar
from common.vectors import Vector2
from part_one import MountainRange, MountainPeak


@dataclass
class MountainNode(MountainPeak):
    parent: Self | None = field(default=None, compare=False)

    steps: int | float = field(default=float("inf"), compare=False)  # steps to get from here to end
    considered: bool = False

    def __repr__(self) -> str:
        return f"Node for {super().__repr__()}"


class NodeMountainRange(MountainRange):
    peak_class = MountainNode

    @staticmethod
    def is_pathable(to_peak: MountainPeak, from_peak: MountainPeak) -> bool:
        height_difference = to_peak.height - from_peak.height
        return height_difference <= 1


class MountainPathfinder:
    weight_per_step: ClassVar[int] = 1

    def __init__(self, grid: NodeMountainRange) -> None:
        self.grid: NodeMountainRange = grid
        self.nodes_to_consider: [MountainNode] = []  # the "open" list

        self.nodes_to_consider.append(self.grid.end_peak)
        self.grid.end_peak.steps = 0

    @staticmethod
    def find_node_of_peak(peak: MountainPeak, list_of_nodes: [MountainNode]) -> MountainNode:
        for node in list_of_nodes:
            if node.peak == peak:
                return node
        raise ValueError

    def find_peak_in_open_list(self, peak: MountainPeak) -> MountainNode:
        return self.find_node_of_peak(peak, self.nodes_to_consider)

    def consider_node(self, node: MountainNode) -> None:
        adjacent_peaks = self.grid.pathable_peaks(node)
        for successor in adjacent_peaks:

            if successor in self.nodes_to_consider:
                if successor.steps <= node.steps + 1:
                    continue
                successor.parent = node
                successor.steps = node.steps + 1
                continue

            if successor.considered:
                if successor.steps <= node.steps + 1:
                    continue
                successor.considered = False

            successor.parent = node
            successor.steps = node.steps + 1
            self.nodes_to_consider.append(successor)
        node.considered = True

    def pathfinding_step(self):
        node = self.nodes_to_consider.pop(0)
        self.consider_node(node)

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

    def all_nodes_of_elevation_a(self):
        return filter(lambda node: node.height == 0, [node for row_of_nodes in self.grid.grid for node in row_of_nodes])

    def node_with_fewest_steps_to_target(self):
        return min(self.all_nodes_of_elevation_a(), key=lambda node: node.steps)


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        mountain_string = input_file.read()

    grid = NodeMountainRange(mountain_string)
    solver = MountainPathfinder(grid)
    solver.pathfind_until_exhausted_solutions()
    result = solver.node_with_fewest_steps_to_target()
    print(f"Fewest steps to target: {result.steps}")
