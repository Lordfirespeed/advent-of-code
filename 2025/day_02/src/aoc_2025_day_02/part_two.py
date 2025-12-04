from typing import Generator, Iterable

from .problem import ProblemInstance


class PartTwoSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    def all_numbers_of_length(self, length: int) -> Iterable[int]:
        return range(10 ** (length - 1), 10 ** length)

    def generate_invalid_ids_of_length(self, length: int) -> Generator[int]:
        half_length, remainder = divmod(length, 2)

        if remainder == 0:
            yield from (int(f"{x}{x}") for x in self.all_numbers_of_length(half_length))
            return

        for middle_number in range(10):
            yield from (int(f"{x}{middle_number}{x}") for x in self.all_numbers_of_length(half_length))

    def solve(self) -> int:
        return len(self.instance.input_plaintext)
