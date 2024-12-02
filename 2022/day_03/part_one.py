from string import ascii_lowercase, ascii_uppercase


class Backpack:
    def __init__(self, backpack_string: str) -> None:
        midpoint_index = len(backpack_string) // 2
        self.first_compartment = set(backpack_string[:midpoint_index])
        self.second_compartment = set(backpack_string[midpoint_index:])

    def item_in_both_compartments(self) -> str:
        intersect = self.first_compartment.intersection(self.second_compartment)
        return intersect.pop()


class Solution:
    def __init__(self, backpacks: [str]) -> None:
        self.backpack_strings = backpacks
        self.backpacks = map(Backpack, self.backpack_strings)

    @staticmethod
    def score_item(item: str) -> int:
        try:
            return ascii_lowercase.index(item) + 1
        except ValueError:
            pass

        try:
            return ascii_uppercase.index(item) + 27
        except ValueError:
            pass

        raise ValueError


    def priority_sum(self):
        return sum([self.score_item(backpack.item_in_both_compartments()) for backpack in self.backpacks])


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        backpacks = [line.strip() for line in input_file.readlines()]

    solver = Solution(backpacks)
    result = solver.priority_sum()
    print(f"Sum of priorities of doubly-placed items: {result}")
