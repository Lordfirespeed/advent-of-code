class CorruptedFourDigitDisplay:
    def __init__(self, inputString):
        signalsString, digitsString = inputString.split(" | ")
        self.signals = signalsString.split(" ")
        self.digits = digitsString.split(" ")


class Solution:
    mapSegmentNumberToDisplayedNumber = {2: 1, 4: 4, 3: 7, 7: 8}

    def count_easy_digits(self, displays: [CorruptedFourDigitDisplay]) -> int:
        count = 0
        for display in displays:
            for displayedDigit in display.digits:
                if len(displayedDigit) in self.mapSegmentNumberToDisplayedNumber.keys():
                    count += 1

        return count


if __name__ == "__main__":
    with open(r"Input\2021day8.txt") as inputFile:
        inputLines = [line.strip() for line in inputFile.readlines()]

    displays = [CorruptedFourDigitDisplay(line) for line in inputLines]

    solver = Solution()
    result = solver.count_easy_digits(displays)
    print(f"Number of 1,4,7,8s: {result}")
