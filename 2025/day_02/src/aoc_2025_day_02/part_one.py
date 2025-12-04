import bisect
import itertools
from typing import Generator, Iterable, Sequence

from util.span import span
from .problem import ProblemInstance


class PartOneSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    def all_numbers_of_length(self, length: int) -> Iterable[int]:
        return range(10 ** (length - 1), 10 ** length)

    def generate_invalid_ids_of_length(self, length: int) -> Generator[int]:
        half_length, remainder = divmod(length, 2)

        if remainder == 1:
            return

        yield from (int(f"{x}{x}") for x in self.all_numbers_of_length(half_length))

    def find_invalid_ids_in_range(self, id_range: span) -> Sequence[int]:
        invalid_ids = list(itertools.chain(*(self.generate_invalid_ids_of_length(length) for length in range(len(str(id_range.start)), len(str(id_range.stop))+1))))
        count_from = bisect.bisect_left(invalid_ids, id_range.start)
        count_to = bisect.bisect_right(invalid_ids, id_range.stop)
        return invalid_ids[count_from:count_to]

    def solve(self) -> int:
        invalid_id_total = 0
        for id_range in self.instance.ranges:
            invalid_id_total += sum(self.find_invalid_ids_in_range(id_range))
        return invalid_id_total
