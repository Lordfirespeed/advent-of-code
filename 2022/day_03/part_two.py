from string import ascii_lowercase, ascii_uppercase


class Backpack:
    def __init__(self, backpack_string: str) -> None:
        self.contains = set(backpack_string)


class BackpackGroup:
    def __init__(self, backpacks: [Backpack]) -> None:
        self.backpacks = backpacks

    def badge_item_type(self):
        backpacks_contents = [backpack.contains for backpack in self.backpacks]
        items_in_all_backpacks = set.intersection(*backpacks_contents)
        return items_in_all_backpacks.pop()


class Solution:
    def __init__(self, backpacks: [str]) -> None:
        self.backpack_strings = backpacks
        self.backpacks = list(map(Backpack, self.backpack_strings))
        self.groups = map(BackpackGroup, batched(self.backpacks, 3))

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
        return sum([self.score_item(group.badge_item_type()) for group in self.groups])


def batched(a_list: list, batch_size: int) -> list[list]:
    for index in range(0, len(a_list), batch_size):
        yield a_list[index:index+batch_size]


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        backpacks = [line.strip() for line in input_file.readlines()]

    solver = Solution(backpacks)
    result = solver.priority_sum()
    print(f"Sum of priorities of badge item types: {result}")
