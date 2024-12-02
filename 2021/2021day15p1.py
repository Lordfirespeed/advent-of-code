from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class Solution:
    def __init__(self, inputLines):
        self.matrix = [[int(digit) for digit in line] for line in inputLines]
        self.grid = Grid(matrix=self.matrix)
        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.never)

    def find_path_of_lowest_risk(self):
        start = self.grid.node(0, 0)
        end = self.grid.node(self.grid.width-1, self.grid.height-1)
        path, runs = self.finder.find_path(start, end, self.grid)
        return path

    def get_risk_coefficient_of_lowest_risk_path(self):
        path = self.find_path_of_lowest_risk()
        totalRisk = 0
        for x, y in path[1:]:
            totalRisk += self.matrix[y][x]
        return totalRisk


if __name__ == "__main__":
    with open(r"Input\2021day15.txt") as inputFile:
        inputLines = [line.strip() for line in inputFile.readlines()]

    solver = Solution(inputLines)
    result = solver.get_risk_coefficient_of_lowest_risk_path()
    print(f"Risk coefficient of lowest risk path: {result}")
