import numpy
from numpy.typing import ArrayLike


class Solution:
    def __init__(self, tree_heights: [[int]]) -> None:
        self.tree_heights = numpy.array(tree_heights)
        self.visible_trees = numpy.full(self.tree_heights.shape, False)

    @staticmethod
    def consider_sequence(heights: [int], visibility: [int]) -> None:
        tallest_seen = heights[0]
        visibility[0] = True
        for index, tree_height in enumerate(heights[1:], 1):
            if tree_height <= tallest_seen:
                continue

            tallest_seen = tree_height
            visibility[index] = True

    def consider_column(self, index: int) -> None:
        self.consider_sequence(self.tree_heights[:, index], self.visible_trees[:, index])
        self.consider_sequence(self.tree_heights[::-1, index], self.visible_trees[::-1, index])

    def consider_row(self, index: int) -> None:
        self.consider_sequence(self.tree_heights[index, :], self.visible_trees[index, :])
        self.consider_sequence(self.tree_heights[index, ::-1], self.visible_trees[index, ::-1])

    def consider_all_columns(self):
        for column_index in range(1, self.tree_heights.shape[0]-1):
            self.consider_column(column_index)

    def consider_all_rows(self):
        for row_index in range(1, self.tree_heights.shape[1]-1):
            self.consider_row(row_index)

    def set_corners_visible(self):
        self.visible_trees[0, 0] = True
        self.visible_trees[0, -1] = True
        self.visible_trees[-1, 0] = True
        self.visible_trees[-1, -1] = True

    def consider(self):
        self.set_corners_visible()
        self.consider_all_columns()
        self.consider_all_rows()

    def num_visible_trees(self) -> int:
        return [tree for row_of_trees in self.visible_trees for tree in row_of_trees].count(True)


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        tree_height_strings = [line.strip() for line in input_file]

    tree_heights = [[int(char) for char in line] for line in tree_height_strings]

    solver = Solution(tree_heights)
    solver.consider()
    result = solver.num_visible_trees()
    print(f"Number of visible trees: {result}")
