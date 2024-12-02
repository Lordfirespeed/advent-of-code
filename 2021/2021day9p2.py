class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __abs__(self):
        return abs(self.x) + abs(self.y)

    def __add__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x + other.x, self.y + other.y)
        elif type(other) == int:
            return Vector2(self.x + other, self.y + other)

    def __sub__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x - other.x, self.y - other.y)
        elif type(other) == int:
            return Vector2(self.x - other, self.y - other)

    def __mul__(self, other):
        if type(other) == Vector2:
            return self.x * other.x + self.y * other.y
        elif type(other) == int:
            return Vector2(self.x * other, self.y * other)

    def __repr__(self):
        return f"({self.x}, {self.y})"


class CaveHeightPoint:
    def __init__(self, height, position):
        self.height = int(height)
        self.position = position
        self.basinConsidered = False
        self.basin = None

    def __repr__(self):
        return f"<{self.position}: {self.height}>"


class Solution:
    neighborDeltas = [Vector2(0, 1), Vector2(0, -1), Vector2(1, 0), Vector2(-1, 0)]

    def __init__(self, inputLines):
        self.numbers = [[CaveHeightPoint(digit, Vector2(xIndex, yIndex)) for xIndex, digit in enumerate(line)] for yIndex, line in enumerate(inputLines)]
        self.ySize = len(self.numbers)
        self.xSize = len(self.numbers[0])

        self.basins = []

    def get_point_at_position(self, position: Vector2):
        return self.numbers[position.y][position.x]

    def get_height_at_position(self, position: Vector2):
        return self.get_point_at_position(position).height

    def get_neighbor_points_of_position(self, position: Vector2):
        neighborPoints = []
        for positionDelta in self.neighborDeltas:
            neighborPosition = position + positionDelta
            if 0 <= neighborPosition.x < self.xSize and 0 <= neighborPosition.y < self.ySize:
                neighborPoint = self.get_point_at_position(neighborPosition)
                neighborPoints.append(neighborPoint)

        return neighborPoints

    def get_neighbor_heights_of_position(self, position: Vector2):
        return [point.height for point in self.get_neighbor_points_of_position(position)]

    def check_position_is_low_point(self, position: Vector2):
        positionValue = self.get_height_at_position(position)
        return all([positionValue < neighborValue for neighborValue in self.get_neighbor_heights_of_position(position)])

    def add_point_to_basin(self, point, basin):
        basin.append(point)
        point.basinConsidered = True
        for neighborPoint in self.get_neighbor_points_of_position(point.position):
            if neighborPoint.height != 9 and neighborPoint.height > point.height and not neighborPoint.basinConsidered:
                self.add_point_to_basin(neighborPoint, basin)

    def add_new_basin_from_low_point_position(self, lowPosition: Vector2):
        lowPoint = self.get_point_at_position(lowPosition)
        newBasin = []
        self.basins.append(newBasin)

        self.add_point_to_basin(lowPoint, newBasin)

    def find_all_basins(self):
        for y in range(self.ySize):
            for x in range(self.xSize):
                position = Vector2(x, y)
                if self.check_position_is_low_point(position):
                    self.add_new_basin_from_low_point_position(position)

    def get_three_largest_basin_size_product(self):
        if not self.basins:
            self.find_all_basins()

        basinSizes = [len(basin) for basin in self.basins]
        sortedBasinSizes = sorted(basinSizes, reverse=True)
        threeLargestBasins = sortedBasinSizes[:4]

        return threeLargestBasins[0] * threeLargestBasins[1] * threeLargestBasins[2]


if __name__ == "__main__":
    with open(r"Input\2021day9.txt") as inputFile:
        inputLines = [line.strip() for line in inputFile.readlines()]

    solver = Solution(inputLines)
    result = solver.get_three_largest_basin_size_product()
    print(f"Three largest basin size product: {result}")
