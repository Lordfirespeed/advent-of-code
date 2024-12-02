from math import floor, ceil


class SnailfishNumber:
    def __init__(self, leftElement, rightElement):
        self.leftElement = leftElement
        if type(leftElement) == SnailfishNumber:
            leftElement.parent = self
        self.rightElement = rightElement
        if type(rightElement) == SnailfishNumber:
            rightElement.parent = self
        self.parent = None

    def __add__(self, other):
        if type(other) == SnailfishNumber:
            sumResult = SnailfishNumber(self, other)
            sumResult.reduce()
            return sumResult
        else:
            raise TypeError

    def __repr__(self):
        return f"[{self.leftElement},{self.rightElement}]"

    def add_to_furthest_to_left(self, value: int):
        if type(self.leftElement) == SnailfishNumber:
            self.leftElement.add_to_furthest_to_left(value)
        else:
            self.leftElement += value

    def add_to_furthest_to_right(self, value: int):
        if type(self.rightElement) == SnailfishNumber:
            self.rightElement.add_to_furthest_to_right(value)
        else:
            self.rightElement += value

    def add_to_closest_to_left(self, value: int):
        if not self.parent:
            pass
        elif self.parent.leftElement is self:
            self.parent.add_to_closest_to_left(value)
        elif type(self.parent.leftElement) == int:
            self.parent.leftElement += value
        else:
            self.parent.leftElement.add_to_furthest_to_right(value)

    def add_to_closest_to_right(self, value: int):
        if not self.parent:
            pass
        elif self.parent.rightElement is self:
            self.parent.add_to_closest_to_right(value)
        elif type(self.parent.rightElement) == int:
            self.parent.rightElement += value
        else:
            self.parent.rightElement.add_to_furthest_to_left(value)

    def replace_with_zero_in_parent(self):
        if self.parent.leftElement is self:
            self.parent.leftElement = 0
        else:
            self.parent.rightElement = 0

    def explode(self):
        self.add_to_closest_to_left(self.leftElement)
        self.add_to_closest_to_right(self.rightElement)
        self.replace_with_zero_in_parent()

    def potentially_explode(self, depth=0):
        if depth >= 4 and type(self.leftElement) == int and type(self.rightElement) == int:
            self.explode()
            return True
        elif type(self.leftElement) == SnailfishNumber and self.leftElement.potentially_explode(depth+1):
            return True
        elif type(self.rightElement) == SnailfishNumber and self.rightElement.potentially_explode(depth+1):
            return True
        else:
            return False

    def potentially_split_elements(self):
        if type(self.leftElement) == SnailfishNumber and self.leftElement.potentially_split_elements():
            return True
        elif type(self.leftElement) == int and self.leftElement >= 10:
            self.leftElement = self.get_snailfish_number_from_splitting_integer(self.leftElement)
            return True
        elif type(self.rightElement) == SnailfishNumber and self.rightElement.potentially_split_elements():
            return True
        elif type(self.rightElement) == int and self.rightElement >= 10:
            self.rightElement = self.get_snailfish_number_from_splitting_integer(self.rightElement)
            return True
        else:
            return False

    def reduce(self):
        actionTaken = True
        while actionTaken:
            actionTaken = self.potentially_explode()
            if actionTaken:
                continue
            actionTaken = self.potentially_split_elements()

    def magnitude(self):
        leftMagnitude = self.get_element_magnitude(self.leftElement)
        rightMagnitude = self.get_element_magnitude(self.rightElement)
        return (3 * leftMagnitude) + (2 * rightMagnitude)

    def get_snailfish_number_from_splitting_integer(self, value):
        valueDividedByTwo = value / 2
        leftElement = floor(valueDividedByTwo)
        rightElement = ceil(valueDividedByTwo)
        newSnailfishNumber = SnailfishNumber(leftElement, rightElement)
        newSnailfishNumber.parent = self
        return newSnailfishNumber

    @staticmethod
    def get_element_magnitude(element):
        if type(element) == SnailfishNumber:
            return element.magnitude()
        elif type(element) == int:
            return element


class Solution:
    def __init__(self, inputLines):
        self.inputLines = inputLines
        self.snailfishNumbers = [self.create_snailfish_number_object_from_string(line) for line in self.inputLines]
        self.sum = None

    @staticmethod
    def find_snailfish_number_string_top_depth_comma(snailfishNumberString: str):
        depth = 0
        splitIndex = None
        for index, character in enumerate(snailfishNumberString):
            if character == ",":
                if depth == 1:
                    splitIndex = index
                    break
            elif character == "[":
                depth += 1
            elif character == "]":
                depth -= 1

        return splitIndex

    @staticmethod
    def create_snailfish_number_object_from_string(snailfishNumberString: str):
        if snailfishNumberString.isdigit():
            return int(snailfishNumberString)

        splitIndex = Solution.find_snailfish_number_string_top_depth_comma(snailfishNumberString)
        leftElementString, rightElementString = snailfishNumberString[1:splitIndex], snailfishNumberString[splitIndex+1:-1]
        leftElement = Solution.create_snailfish_number_object_from_string(leftElementString)
        rightElement = Solution.create_snailfish_number_object_from_string(rightElementString)

        return SnailfishNumber(leftElement, rightElement)

    def sum_all_snailfish_numbers(self):
        self.sum = self.snailfishNumbers[0]
        for snailfishNumber in self.snailfishNumbers[1:]:
            self.sum = self.sum + snailfishNumber

    def get_final_sum_magnitude(self):
        self.sum_all_snailfish_numbers()
        return self.sum.magnitude()


if __name__ == "__main__":
    with open(r"Input\2021day18.txt") as inputFile:
        inputLines = [line.strip() for line in inputFile.readlines()]

    solver = Solution(inputLines)
    result = solver.get_final_sum_magnitude()
    print(f"Homework final sum magnitude: {result}")
