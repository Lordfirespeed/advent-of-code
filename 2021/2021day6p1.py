class Solution:
    def __init__(self):
        self.fish = []

    def simulate(self, startFish, cycles):
        self.fish = startFish.copy()

        for cycleIndex in range(cycles):
            numFishToAdd = 0
            for fishIndex, thisFish in enumerate(self.fish):
                if thisFish == 0:
                    numFishToAdd += 1
                    self.fish[fishIndex] = 6
                else:
                    self.fish[fishIndex] -= 1

            self.fish += [8] * numFishToAdd

        return len(self.fish)


if __name__ == "__main__":
    with open(r"Input\2021day6.txt") as inputFile:
        inputNums = [int(number) for number in inputFile.readline().strip().split(",")]

    solver = Solution()
    result = solver.simulate(inputNums, 80)
    print(f"There are {result} fish after 80 cycles.")

