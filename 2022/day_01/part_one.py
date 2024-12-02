class Solution:
    def __init__(self, elves: [[int]]) -> None:
        self.elves = elves

    def most_calorific(self) -> int:
        calorie_totals = map(sum, self.elves)
        return max(calorie_totals)


if __name__ == "__main__":
    with open(r"input.txt") as inputFile:
        elves = inputFile.read().split("\n\n")

    elves = map(lambda x: x.split("\n"), elves)
    elves = [list(map(int, elf)) for elf in elves]

    solver = Solution(elves)
    result = solver.most_calorific()
    print(f"Most calorific elf is carrying {result} calories")
