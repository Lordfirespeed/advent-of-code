class ElfPair:
    def __init__(self, assignment_string: str) -> None:
        first_range_string, second_range_string = assignment_string.split(",")
        self.first_range = self.range_from_range_string(first_range_string)
        self.second_range = self.range_from_range_string(second_range_string)

    @staticmethod
    def range_from_range_string(range_string: str) -> slice:
        start_string, end_string = range_string.split("-")
        return slice(int(start_string), int(end_string))

    @staticmethod
    def a_contains_b(a: slice, b: slice) -> bool:
        return a.start <= b.start and a.stop >= b.stop

    def first_contains_second(self) -> bool:
        return self.a_contains_b(self.first_range, self.second_range)

    def second_contains_first(self) -> bool:
        return self.a_contains_b(self.second_range, self.first_range)

    def assignment_fully_overlaps(self) -> bool:
        return self.first_contains_second() or self.second_contains_first()


class Solution:
    def __init__(self, elf_assignments: [str]) -> None:
        self.elf_pairs = list(map(ElfPair, elf_assignments))

    def count_full_overlaps(self):
        return [pair.assignment_fully_overlaps() for pair in self.elf_pairs].count(True)


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        input_lines = [line.strip() for line in input_file.readlines()]

    solver = Solution(input_lines)
    result = solver.count_full_overlaps()
    print(f"Number of assignment pairs with complete overlaps: {result}")
