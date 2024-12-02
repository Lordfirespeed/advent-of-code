class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def horizontalFold(self, positionOnAxis):
        if self.y > positionOnAxis:
            newYPosition = (2 * positionOnAxis) - self.y
            self.y = newYPosition

    def verticalFold(self, positionOnAxis):
        if self.x > positionOnAxis:
            newXPosition = (2 * positionOnAxis) - self.x
            self.x = newXPosition

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

    def __eq__(self, other):
        if type(other) != Vector2:
            raise TypeError
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Solution:
    def __init__(self, inputString):
        stringDotPositions, wholeFoldInstructions = inputString.split("\n\n")
        tupleDotPositions = [tuple([int(number) for number in position.split(",")]) for position in stringDotPositions.split("\n")]
        self.dotPositions = [Vector2(*tuplePosition) for tuplePosition in tupleDotPositions]
        usefulPartOfFoldInstructions = [foldInstruction[11:].split("=") for foldInstruction in wholeFoldInstructions.split("\n")]
        self.foldInstructions = [(axis, int(positionOnAxis)) for axis, positionOnAxis in usefulPartOfFoldInstructions]

    def horizontalFold(self, positionOnAxis):
        for dotPosition in self.dotPositions:
            dotPosition.horizontalFold(positionOnAxis)

    def verticalFold(self, positionOnAxis):
        for dotPosition in self.dotPositions:
            dotPosition.verticalFold(positionOnAxis)

    def fold(self, axis, positionOnAxis):
        if axis == "x":
            self.verticalFold(positionOnAxis)
        else:
            self.horizontalFold(positionOnAxis)

    def execute_current_fold_instruction(self):
        instruction = self.foldInstructions.pop(0)
        self.fold(instruction[0], instruction[1])

    def get_number_of_visible_dots(self):
        discreteDotPositions = []
        for dotPosition in self.dotPositions:
            alreadyConsideredVisible = False
            for otherPosition in discreteDotPositions:
                if dotPosition == otherPosition:
                    alreadyConsideredVisible = True
                    break
            if not alreadyConsideredVisible:
                discreteDotPositions.append(dotPosition)

        return len(discreteDotPositions)


if __name__ == "__main__":
    with open(r"Input\2021day13.txt") as inputFile:
        inputString = "".join([line for line in inputFile.readlines()])

    solver = Solution(inputString)
    solver.execute_current_fold_instruction()
    result = solver.get_number_of_visible_dots()
    print(f"Number of visible dots after first fold instruction: {result}")
