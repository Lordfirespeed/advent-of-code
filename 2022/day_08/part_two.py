import numpy
from enum import Enum


class Direction(Enum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3


class Solution:
    def __init__(self, tree_heights: [[int]]) -> None:
        self.tree_heights = numpy.array(tree_heights)
        self.tree_visibility = numpy.full((4, *self.tree_heights.shape), 0)

    @staticmethod
    def consider_sequence(heights: [int], visibility: [int]) -> None:
        blocking_indexes = numpy.empty(heights.shape, int)
        blocking_indexes[0] = 0
        for tree_index, tree_height in enumerate(heights[1:], 1):
            blocked_by_index = tree_index-1
            while heights[blocked_by_index] < tree_height and blocked_by_index > 0:
                blocked_by_index = blocking_indexes[blocked_by_index]
            blocking_indexes[tree_index] = blocked_by_index

            visibility[tree_index] = tree_index - blocked_by_index

    def consider_column(self, index: int) -> None:
        self.consider_sequence(self.tree_heights[:, index], self.tree_visibility[Direction.Up.value, :, index])
        self.consider_sequence(self.tree_heights[::-1, index], self.tree_visibility[Direction.Down.value, ::-1, index])

    def consider_row(self, index: int) -> None:
        self.consider_sequence(self.tree_heights[index, :], self.tree_visibility[Direction.Left.value, index, :])
        self.consider_sequence(self.tree_heights[index, ::-1], self.tree_visibility[Direction.Right.value, index, ::-1])

    def consider_all_columns(self):
        for column_index in range(0, self.tree_heights.shape[0]):
            self.consider_column(column_index)

    def consider_all_rows(self):
        for row_index in range(0, self.tree_heights.shape[1]):
            self.consider_row(row_index)

    def consider(self):
        self.consider_all_columns()
        self.consider_all_rows()

    def scenic_scores(self):
        scores = numpy.empty(self.tree_heights.shape, int)

        for y in range(self.tree_heights.shape[0]):
            for x in range(self.tree_heights.shape[1]):
                scores[y, x] = numpy.prod(self.tree_visibility[:, y, x])

        return scores

    def maximum_scenic_score(self) -> int:
        return numpy.max(self.scenic_scores())


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        tree_height_strings = [line.strip() for line in input_file]

    tree_heights = [[int(char) for char in line] for line in tree_height_strings]

    solver = Solution(tree_heights)
    solver.consider()
    result = solver.maximum_scenic_score()
    print(f"Maximum scenic score: {result}")
