from sympy import symbols, solve
from math import sqrt, ceil, floor

x, y = symbols("x y")


class Solution:
    def __init__(self, inputLine: str):
        self.areaString = inputLine[13:]
        xRangeString, yRangeString = self.areaString.split(", ")
        xMinString, xMaxString = xRangeString[2:].split("..")
        self.xRange = (int(xMinString), int(xMaxString))
        yMinString, yMaxString = yRangeString[2:].split("..")
        self.yRange = (int(yMinString), int(yMaxString))

    @staticmethod
    def inverse_triangular_number(number):
        return sqrt(2 * number + 0.25) - 0.5

    def find_terminating_initial_x_values(self):
        minInitialX = ceil(self.inverse_triangular_number(self.xRange[0]))
        maxInitialX = floor(self.inverse_triangular_number(self.xRange[1]))
        return range(minInitialX, maxInitialX+1)

    def find_(self):
        pass

    def find_highest_y_position_trajectory(self):
        xStarts = self.find_terminating_initial_x_values()
        for yEnd in range(*self.yRange):
            yStartEq = (yEnd + (x * (x + 1) / 2)) - (y * (x + 1))



if __name__ == "__main__":
    with open(r"Input\2021day17test.txt") as inputFile:
        inputLine = inputFile.readline().strip()

    solver = Solution(inputLine)
    result = solver.foo()
    print(f"foo: {result}")
