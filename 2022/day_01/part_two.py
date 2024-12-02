class Solution:
    def __init__(self, elves: [[int]]) -> None:
        self.elves = elves

    def calorie_totals(self) -> [int]:
        return list(map(sum, self.elves))

    def most_calorific(self) -> int:
        calorie_totals = self.calorie_totals()
        return max(calorie_totals)

    def top_three_most_calorific(self) -> int:
        calorie_totals = self.calorie_totals()
        calorie_totals.sort(reverse=True)
        return sum(calorie_totals[:3])


if __name__ == "__main__":
    with open(r"input.txt") as inputFile:
        elves = inputFile.read().split("\n\n")

    elves = map(lambda x: x.split("\n"), elves)
    elves = [list(map(int, elf)) for elf in elves]

    solver = Solution(elves)
    print(f"Most calorific elf is carrying {solver.most_calorific()} calories")
    print(f"Top 3 most calorific elves are carrying {solver.top_three_most_calorific()} calories")
