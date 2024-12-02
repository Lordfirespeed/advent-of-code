# 7-segment indexing
#  0000
# 1    2
# 1    2
#  3333
# 4    5
# 4    5
#  6666

class CorruptedFourDigitDisplay:
    mapNumbertoSegmentIndexes = {0: {0, 1, 2, 4, 5, 6},
                                 1: {2, 5},
                                 2: {0, 2, 3, 4, 6},
                                 3: {0, 2, 3, 5, 6},
                                 4: {1, 2, 3, 5},
                                 5: {0, 1, 3, 5, 6},
                                 6: {0, 1, 3, 4, 5, 6},
                                 7: {0, 2, 5},
                                 8: {0, 1, 2, 3, 4, 5, 6},
                                 9: {0, 1, 2, 3, 5, 6}}

    mapNumberOfSegmentsToDigits = {2: [1], 3: [7], 4: [4], 5: [2, 3, 5], 6: [0, 6, 9], 7: [8]}

    characters = "abcdefg"

    def __init__(self, inputString):
        signalsString, digitsString = inputString.split(" | ")
        self.signals = signalsString.split(" ")
        self.digits = digitsString.split(" ")
        self.signalsPossibleDigits = {}
        self.charactersPossibleSegmentIndexes = {}
        self.depletedSegmentIndexes = set()

        self.characterToSegmentSolution = {}
        self.outputValue = None

        for signal in self.signals:
            self.signalsPossibleDigits[signal] = self.mapNumberOfSegmentsToDigits[len(signal)].copy()

        for character in self.characters:
            self.charactersPossibleSegmentIndexes[character] = set(range(7))

    def checkSignalCanDisplayDigit(self, signal, digit):
        expectedSegments = self.mapNumbertoSegmentIndexes[digit].copy()
        for character in signal:
            segmentIntersect = self.charactersPossibleSegmentIndexes[character].intersection(expectedSegments)
            if len(segmentIntersect) == 0:
                return False
            expectedSegments.remove(segmentIntersect.pop())
        return True

    def reduceSignalsPossibleDigits(self):
        for signal, signalPossibleDigits in self.signalsPossibleDigits.items():
            invalidDigits = set()
            for possibleDigit in signalPossibleDigits:
                if not self.checkSignalCanDisplayDigit(signal, possibleDigit):
                    invalidDigits.add(possibleDigit)

            for invalidDigit in invalidDigits:
                signalPossibleDigits.remove(invalidDigit)

    def reduceCharacterPossibleSegmentIndexesBySignals(self):
        for signal, possibleDigits in self.signalsPossibleDigits.items():
            possibleSegmentIndexes = set()
            for possibleDigit in possibleDigits:
                possibleSegmentIndexes = possibleSegmentIndexes.union(self.mapNumbertoSegmentIndexes[possibleDigit])

            for character in signal:
                self.charactersPossibleSegmentIndexes[character] = self.charactersPossibleSegmentIndexes[character].intersection(possibleSegmentIndexes)

    def reduceCharacterPossibleSegmentIndexesByDepletedCharacters(self):
        if self.depletedSegmentIndexes == set(range(7)):
            return

        unchanged = False
        while not unchanged:
            unchanged = True
            for character, possibleSegmentIndexes in self.charactersPossibleSegmentIndexes.items():
                identicalCharacters = [character]
                for otherCharacter, otherPossibleSegmentIndexes in self.charactersPossibleSegmentIndexes.items():
                    if character == otherCharacter:
                        continue
                    elif possibleSegmentIndexes == otherPossibleSegmentIndexes:
                        identicalCharacters.append(otherCharacter)

                if len(identicalCharacters) == len(possibleSegmentIndexes) and not possibleSegmentIndexes.issubset(self.depletedSegmentIndexes):
                    unchanged = False
                    for removePossibleIndex in possibleSegmentIndexes:
                        self.depletedSegmentIndexes.add(removePossibleIndex)
                    for setCharacter, setPossibleSegmentIndexes in self.charactersPossibleSegmentIndexes.items():
                        if setCharacter not in identicalCharacters:
                            for removePossibleIndex in possibleSegmentIndexes:
                                if removePossibleIndex in setPossibleSegmentIndexes:
                                    setPossibleSegmentIndexes.remove(removePossibleIndex)

    def solveCharacterToSegmentMapping(self):
        self.reduceCharacterPossibleSegmentIndexesBySignals()
        self.reduceCharacterPossibleSegmentIndexesByDepletedCharacters()

        while max([len(possibleDigits) for signal, possibleDigits in self.signalsPossibleDigits.items()]) > 1:
            self.reduceCharacterPossibleSegmentIndexesBySignals()
            self.reduceSignalsPossibleDigits()

        self.reduceCharacterPossibleSegmentIndexesBySignals()

        for character, possibleSegmentIndexes in self.charactersPossibleSegmentIndexes.items():
            if possibleSegmentIndexes == {4, 6}:
                self.characterToSegmentSolution[character] = 4
            else:
                self.characterToSegmentSolution[character] = possibleSegmentIndexes.pop()

    def processSignalToInteger(self, signal):
        if not self.characterToSegmentSolution:
            self.solveCharacterToSegmentMapping()

        segments = {self.characterToSegmentSolution[character] for character in signal}

        for digit, expectedSegmentsForDigit in self.mapNumbertoSegmentIndexes.items():
            if segments == expectedSegmentsForDigit:
                return digit
        raise KeyError

    def processOutputValue(self):
        fourDigits = ""

        for digitString in self.digits:
            fourDigits += str(self.processSignalToInteger(digitString))

        self.outputValue = int(fourDigits)

        return self.outputValue


class Solution:
    @staticmethod
    def sum_output_values(displays: [CorruptedFourDigitDisplay]) -> int:
        count = 0
        for display in displays:
            count += display.processOutputValue()

        return count


if __name__ == "__main__":
    with open(r"Input\2021day8.txt") as inputFile:
        inputLines = [line.strip() for line in inputFile.readlines()]

    displays = [CorruptedFourDigitDisplay(line) for line in inputLines]
    displays[0].solveCharacterToSegmentMapping()

    solver = Solution()
    result = solver.sum_output_values(displays)
    print(f"Sum of output values: {result}")
