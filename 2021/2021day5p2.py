from collections import defaultdict


class Solution:
    def __init__(self):
        self.positions = defaultdict(lambda: defaultdict(lambda: 0))

    def add_fundamental_vent_line_to_positions(self, endPoint1, endPoint2):
        xValues = (endPoint1[0], endPoint2[0])
        yValues = (endPoint1[1], endPoint2[1])

        xMin, xMax = min(xValues), max(xValues)
        yMin, yMax = min(yValues), max(yValues)

        for setX in range(xMin, xMax + 1):
            for setY in range(yMin, yMax + 1):
                self.positions[setY][setX] += 1

    def add_diagonal_vent_line_to_positions(self, endPoint1, endPoint2):
        xStart, xEnd = endPoint1[0], endPoint2[0]
        yStart, yEnd = endPoint1[1], endPoint2[1]
        xDelta = xEnd - xStart
        yDelta = yEnd - yStart
        xDeltaDirection = 1 if xDelta >= 0 else -1
        yDeltaDirection = 1 if yDelta >= 0 else -1

        xValues = range(xStart, xEnd+xDeltaDirection, xDeltaDirection)
        yValues = range(yStart, yEnd+yDeltaDirection, yDeltaDirection)

        for xSet, ySet in zip(xValues, yValues):
            self.positions[ySet][xSet] += 1

    def add_vent_line_to_positions(self, endPoint1, endPoint2):
        if endPoint1[0] == endPoint2[0] or endPoint1[1] == endPoint2[1]:
            self.add_fundamental_vent_line_to_positions(endPoint1, endPoint2)
        else:
            self.add_diagonal_vent_line_to_positions(endPoint1, endPoint2)

    def find_dangerous_areas_of_coordinate_pairs(self, coordinatePairs):
        # set position vent coefficients
        for endPoint1, endPoint2 in coordinatePairs:
            self.add_vent_line_to_positions(endPoint1, endPoint2)

        # find positions with danger > 1

        dangerousPositionCount = 0
        for row in self.positions.values():
            for positionCoefficient in row.values():
                if positionCoefficient > 1:
                    dangerousPositionCount += 1

        return dangerousPositionCount

    @staticmethod
    def make_coordinate_pairs_from_input_lines(inputLines):
        stringCoordinates = [line.split(" -> ") for line in inputLines]
        stringTupleCoordinatePairs = [tuple([tuple(stringCoordinate.split(",")) for stringCoordinate in line]) for line in stringCoordinates]
        numberTupleCoordinatePairs = [tuple([tuple([int(stringNumber) for stringNumber in stringTupleCoordinate]) for stringTupleCoordinate in line]) for line in stringTupleCoordinatePairs]

        return numberTupleCoordinatePairs

    def find_dangerous_areas_of_input_lines(self, inputLines):
        coordinatePairs = self.make_coordinate_pairs_from_input_lines(inputLines)
        return self.find_dangerous_areas_of_coordinate_pairs(coordinatePairs)


if __name__ == "__main__":
    with open(r"Input\2021day5.txt") as inputFile:
        inputLines = [line.strip() for line in inputFile.readlines()]

    solver = Solution()
    result = solver.find_dangerous_areas_of_input_lines(inputLines)
    print(f"Found {result} dangerous positions.")
