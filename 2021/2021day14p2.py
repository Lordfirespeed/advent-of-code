from collections import defaultdict


class Solution:
    def __init__(self, inputLines):
        self.initialPolymer = inputLines[0]
        pairInsertionRuleStrings = inputLines[2:]
        self.pairInsertionRules = dict([ruleString.split(" -> ") for ruleString in pairInsertionRuleStrings])
        self.currentPolymerPairs = self.pairs(self.initialPolymer)

    @staticmethod
    def pairs(polymer):
        pairs = defaultdict(lambda: 0)
        for pair in [polymer[index:index+2] for index in range(len(polymer)-1)]:
            pairs[pair] += 1
        return pairs

    def execute_single_insertion_step(self):
        newPairs = defaultdict(lambda: 0)

        for insertToPair, toInsert in self.pairInsertionRules.items():
            numberOfInsertToPairInPolymer = self.currentPolymerPairs[insertToPair]
            if numberOfInsertToPairInPolymer > 0:
                createdLeftPair = insertToPair[0] + toInsert
                createdRightPair = toInsert + insertToPair[1]
                newPairs[createdLeftPair] += numberOfInsertToPairInPolymer
                newPairs[createdRightPair] += numberOfInsertToPairInPolymer

                self.currentPolymerPairs[insertToPair] = 0

        for newPair, numberOfNewPair in newPairs.items():
            self.currentPolymerPairs[newPair] += numberOfNewPair

    def execute_multiple_insertion_steps(self, numberOfSteps):
        for _ in range(numberOfSteps):
            self.execute_single_insertion_step()

    def countElements(self):
        elementCounts = defaultdict(lambda: 0)

        elementCounts[self.initialPolymer[0]] += 1

        for pair, numberOfPair in self.currentPolymerPairs.items():
            elementCounts[pair[1]] += numberOfPair

        return elementCounts

    def most_common_minus_least_common_element(self):
        elementCounts = self.countElements().values()
        return max(elementCounts) - min(elementCounts)


if __name__ == "__main__":
    with open(r"Input\2021day14.txt") as inputFile:
        inputLines = [line.strip() for line in inputFile.readlines()]

    solver = Solution(inputLines)
    steps = 40
    solver.execute_multiple_insertion_steps(steps)
    result = solver.most_common_minus_least_common_element()
    print(f"Most common - least common element after {steps} insertion steps: {result}")
