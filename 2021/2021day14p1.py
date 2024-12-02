from collections import defaultdict


class Solution:
    def __init__(self, inputLines):
        self.initialPolymer = inputLines[0]
        pairInsertionRuleStrings = inputLines[2:]
        self.pairInsertionRules = dict([ruleString.split(" -> ") for ruleString in pairInsertionRuleStrings])

        self.currentPolymer = list(self.initialPolymer)

    def execute_single_insertion_step(self):
        for positionIndex in range(len(self.currentPolymer)-1, 0, -1):
            pair = "".join(self.currentPolymer[positionIndex-1:positionIndex+1])
            try:
                toInsert = self.pairInsertionRules[pair]
                self.currentPolymer.insert(positionIndex, toInsert)
            except KeyError:
                pass

    def execute_multiple_insertion_steps(self, numberOfSteps):
        for _ in range(numberOfSteps):
            self.execute_single_insertion_step()

    def countElements(self):
        elementCounts = defaultdict(lambda: 0)

        for element in self.currentPolymer:
            elementCounts[element] += 1

        return elementCounts

    def most_common_minus_least_common_element(self):
        elementCounts = self.countElements().values()
        return max(elementCounts) - min(elementCounts)


if __name__ == "__main__":
    with open(r"Input\2021day14.txt") as inputFile:
        inputLines = [line.strip() for line in inputFile.readlines()]

    solver = Solution(inputLines)
    steps = 10
    solver.execute_multiple_insertion_steps(steps)
    result = solver.most_common_minus_least_common_element()
    print(f"Most common - least common element after {steps} insertion steps: {result}")
