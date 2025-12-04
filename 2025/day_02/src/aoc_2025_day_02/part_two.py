import bisect
import itertools
from typing import Generator, Iterable, Sequence

from util.span import span
from .problem import ProblemInstance


class PartTwoSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    def all_numbers_of_length(self, length: int) -> Iterable[int]:
        return range(10 ** (length - 1), 10 ** length)

    def generate_invalid_ids_of_length_with_repeating_unit_length(self, length: int, repeating_unit_length: int) -> Generator[int]:
        repeats, remainder = divmod(length, repeating_unit_length)

        if repeats < 2: return
        if remainder != 0: return

        yield from (int(str(x) * repeats) for x in self.all_numbers_of_length(repeating_unit_length))

    def find_invalid_ids_in_range_with_repeating_unit_length(self, id_range: span, repeating_unit_length: int) -> Sequence[int]:
        invalid_ids = list(itertools.chain(*(self.generate_invalid_ids_of_length_with_repeating_unit_length(length, repeating_unit_length) for length in range(len(str(id_range.start)), len(str(id_range.stop))+1))))
        count_from = bisect.bisect_left(invalid_ids, id_range.start)
        count_to = bisect.bisect_right(invalid_ids, id_range.stop)
        return invalid_ids[count_from:count_to]

    def find_invalid_ids_in_range(self, id_range: span) -> Generator[int]:
        seen_invalid_ids: set[int] = set()

        for repeating_unit_length in range(1, (len(str(id_range.stop)) // 2) + 1):
            for invalid_id in self.find_invalid_ids_in_range_with_repeating_unit_length(id_range, repeating_unit_length):
                if invalid_id in seen_invalid_ids: continue
                seen_invalid_ids.add(invalid_id)
                yield invalid_id

    def solve(self) -> int:
        invalid_id_total = 0
        for id_range in self.instance.ranges:
            invalid_id_total += sum(self.find_invalid_ids_in_range(id_range))
        return invalid_id_total
