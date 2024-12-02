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


class Solution:
    neighborDeltas = [Vector2(0, 1), Vector2(0, -1), Vector2(1, 0), Vector2(-1, 0)]

    def __init__(self, inputLines):
        self.numbers = [[int(digit) for digit in line] for line in inputLines]
        self.ySize = len(self.numbers)
        self.xSize = len(self.numbers[0])

    def get_height_at_position(self, position: Vector2):
        return self.numbers[position.y][position.x]

    def get_neighbor_heights_of_position(self, position: Vector2):
        neighborValues = []
        for positionDelta in self.neighborDeltas:
            neighborPosition = position + positionDelta
            if 0 <= neighborPosition.x < self.xSize and 0 <= neighborPosition.y < self.ySize:
                neighborValue = self.get_height_at_position(neighborPosition)
                neighborValues.append(neighborValue)

        return neighborValues

    def check_position_is_low_point(self, position: Vector2):
        positionValue = self.get_height_at_position(position)
        return all([positionValue < neighborValue for neighborValue in self.get_neighbor_heights_of_position(position)])

    def get_risk_level_at_position(self, position: Vector2):
        return self.get_height_at_position(position) + 1

    def get_risk_level_sum(self):
        riskLevelSum = 0
        for y in range(self.ySize):
            for x in range(self.xSize):
                position = Vector2(x, y)
                if self.check_position_is_low_point(position):
                    riskLevelSum += self.get_risk_level_at_position(position)

        return riskLevelSum


if __name__ == "__main__":
    with open(r"Input\2021day9.txt") as inputFile:
        inputLines = [line.strip() for line in inputFile.readlines()]

    solver = Solution(inputLines)
    result = solver.get_risk_level_sum()
    print(f"Risk level sum: {result}")
