class Solution:
    def __init__(self):
        self.fish = {num: 0 for num in range(9)}

    def simulate(self, startFish, cycles):
        for thisFish in startFish:
            self.fish[thisFish] += 1

        for cycleIndex in range(cycles):
            numNewFish = self.fish[0]
            for fishTimer in range(1, 9):
                self.fish[fishTimer-1] = self.fish[fishTimer]
            self.fish[8] = numNewFish
            self.fish[6] += numNewFish

        return sum(self.fish.values())


if __name__ == "__main__":
    with open(r"Input\2021day6.txt") as inputFile:
        inputNums = [int(number) for number in inputFile.readline().strip().split(",")]

    cycles = 256
    solver = Solution()
    result = solver.simulate(inputNums, cycles)
    print(f"There are {result} fish after {cycles} cycles.")

