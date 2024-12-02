from collections import defaultdict


class Solution:
    @staticmethod
    def find_dangerous_areas_of_coordinate_pairs(coordinatePairs):
        positions = defaultdict(lambda: defaultdict(lambda: 0))

        # set position vent coefficients
        for endPoint1, endPoint2 in coordinatePairs:
            xValues = (endPoint1[0], endPoint2[0])
            yValues = (endPoint1[1], endPoint2[1])

            xMin, xMax = min(xValues), max(xValues)
            yMin, yMax = min(yValues), max(yValues)

            for setX in range(xMin, xMax+1):
                for setY in range(yMin, yMax+1):
                    positions[setY][setX] += 1

        # find positions with danger > 1

        dangerousPositionCount = 0
        for row in positions.values():
            for positionCoefficient in row.values():
                if positionCoefficient > 1:
                    dangerousPositionCount += 1

        return dangerousPositionCount

    @staticmethod
    def make_coordinate_pairs_from_input_lines(inputLines):
        stringCoordinates = [line.split(" -> ") for line in inputLines]
        stringTupleCoordinatePairs = [tuple([tuple(stringCoordinate.split(",")) for stringCoordinate in line]) for line in stringCoordinates]
        numberTupleCoordinatePairs = [tuple([tuple([int(stringNumber) for stringNumber in stringTupleCoordinate]) for stringTupleCoordinate in line]) for line in stringTupleCoordinatePairs]

        fundamentalDirectionVentLines = [(endPoint1, endPoint2) for endPoint1, endPoint2 in numberTupleCoordinatePairs if endPoint1[0] == endPoint2[0] or endPoint1[1] == endPoint2[1]]

        return fundamentalDirectionVentLines

    def find_dangerous_areas_of_input_lines(self, inputLines):
        coordinatePairs = self.make_coordinate_pairs_from_input_lines(inputLines)
        return self.find_dangerous_areas_of_coordinate_pairs(coordinatePairs)


if __name__ == "__main__":
    with open(r"Input\2021day5.txt") as inputFile:
        inputLines = [line.strip() for line in inputFile.readlines()]

    solver = Solution()
    result = solver.find_dangerous_areas_of_input_lines(inputLines)
    print(f"Found {result} dangerous positions.")
