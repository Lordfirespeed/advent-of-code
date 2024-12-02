from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class Matrix:
    def __init__(self, twoDimensionalList):
        self.matrix = twoDimensionalList

    def copy(self):
        copyOfSelf = Matrix(self.matrix.copy())
        for index, thingAtIndex in enumerate(copyOfSelf.matrix):
            if type(thingAtIndex) == list or type(thingAtIndex) == Matrix:
                copyOfSelf.matrix[index] = thingAtIndex.copy()
        return copyOfSelf

    def add_to_matrix(self, addValue):
        if type(addValue) == int:
            for row in self.matrix:
                for indexOfRow, value in enumerate(row):
                    newValue = value + addValue
                    while newValue >= 10:
                        newValue -= 9
                    row[indexOfRow] = newValue

        else:
            raise TypeError

    def increment_matrix(self):
        self.add_to_matrix(1)


class TiledMatrix:
    def __init__(self, initialTile: Matrix):
        self.initialTile = initialTile.copy()
        self.fullMatrix = self.initialTile.copy()

        self.populate_full_matrix()

    def tile_to_right(self, tile):
        for rowIndex, row in enumerate(tile.matrix):
            self.fullMatrix.matrix[rowIndex] += row

    def tile_downwards(self, row):
        self.fullMatrix.matrix += row.copy().matrix

    def populate_full_matrix(self):
        incrementingTile = self.initialTile.copy()
        for xTileIndex in range(4):
            incrementingTile.increment_matrix()
            self.tile_to_right(incrementingTile)

        incrementingRow = self.fullMatrix.copy()
        for yTileIndex in range(4):
            incrementingRow.increment_matrix()
            self.tile_downwards(incrementingRow)


class Solution:
    def __init__(self, inputLines):
        self.one25thMatrix = Matrix([[int(digit) for digit in line] for line in inputLines])
        self.matrix = TiledMatrix(self.one25thMatrix).fullMatrix.matrix
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
