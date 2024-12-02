class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Octopus:
    def __init__(self, initialEnergy, position):
        self.energy = initialEnergy
        self.position = position
        self.flashed = False

    def __repr__(self):
        return f"<({self.energy}) {'X' if self.flashed else 'O'}>"

    def __str__(self):
        return self.__repr__()


class Solution:
    adjacencyDeltaVectors = [Vector2(1, 1), Vector2(1, 0), Vector2(1, -1), Vector2(0, -1), Vector2(-1, -1), Vector2(-1, 0), Vector2(-1, 1), Vector2(0, 1)]

    def __init__(self, inputLines):
        self.octopusCavern = [[Octopus(int(digit), Vector2(xPos, yPos)) for xPos, digit in enumerate(line)] for yPos, line in enumerate(inputLines)]
        self.totalFlashes = 0
        self.steps = 0
        self.xSize = 10
        self.ySize = 10

    def get_octopus_at_position(self, position):
        return self.octopusCavern[position.y][position.x]

    def get_adjacent_octopi_of_position(self, position):
        adjacentOctopi = []
        for deltaVector in self.adjacencyDeltaVectors:
            neighborPosition = position + deltaVector
            if 0 <= neighborPosition.x < self.xSize and 0 <= neighborPosition.y < self.ySize:
                adjacentOctopi.append(self.get_octopus_at_position(neighborPosition))

        return adjacentOctopi

    def increase_energy_level(self):
        for octopusLine in self.octopusCavern:
            for octopus in octopusLine:
                octopus.energy += 1

    def flash_octopus_at_position(self, position):
        octopus = self.get_octopus_at_position(position)
        if octopus.energy > 9 and not octopus.flashed:
            octopus.flashed = True
            for adjacentOctopus in self.get_adjacent_octopi_of_position(position):
                if position == Vector2(1, 1):
                    print(adjacentOctopus)
                adjacentOctopus.energy += 1
                self.flash_octopus_at_position(adjacentOctopus.position)

    def flash_all_octopi_at_high_energy(self):
        for octopusLine in self.octopusCavern:
            for octopus in octopusLine:
                if octopus.energy > 9 and not octopus.flashed:
                    self.flash_octopus_at_position(octopus.position)

    def reset_flashed_octopi_energy(self):
        for octopusLine in self.octopusCavern:
            for octopus in octopusLine:
                if octopus.flashed:
                    octopus.energy = 0

    def reset_flashed_octopi_flashed(self):
        for octopusLine in self.octopusCavern:
            for octopus in octopusLine:
                if octopus.flashed:
                    octopus.flashed = False
                    self.totalFlashes += 1

    def step_octopus_cavern(self):
        self.increase_energy_level()
        self.flash_all_octopi_at_high_energy()
        self.reset_flashed_octopi_energy()
        self.reset_flashed_octopi_flashed()
        self.steps += 1

    def get_flash_count_after_steps(self, steps):
        for stepIndex in range(steps):
            self.step_octopus_cavern()
        return self.totalFlashes

    def print_octopus_cavern(self):
        print("\n".join([" ".join([str(octopus) for octopus in row]) for row in self.octopusCavern]))
        print()


if __name__ == "__main__":
    with open(r"Input\2021day11.txt") as inputFile:
        inputLines = [line.strip() for line in inputFile.readlines()]

    solver = Solution(inputLines)
    result = solver.get_flash_count_after_steps(100)
    print(f"Number of flashes after {solver.steps} steps: {result}")
