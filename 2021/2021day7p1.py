class Solution:
    def __init__(self):
        self.fuelCosts = []

    @staticmethod
    def calculate_fuel_cost(init, targetPosition):
        return sum([abs(position - targetPosition) for position in init])

    def find_min_fuel_cost(self, initial_positions):
        self.fuelCosts = []
        for position in range(min(initial_positions), max(initial_positions)+1):
            self.fuelCosts.append(self.calculate_fuel_cost(initial_positions, position))

        return min(self.fuelCosts)


if __name__ == "__main__":
    with open(r"Input\2021day7.txt") as inputFile:
        inputNums = [int(number) for number in inputFile.readline().strip().split(",")]

    solver = Solution()
    result = solver.find_min_fuel_cost(inputNums)
    print(f"Minimum fuel cost {result}")
