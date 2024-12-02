from operator import countOf

from .problem import ProblemInstance


class PartOneSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    @classmethod
    def is_increasing(cls, report_diffs: list[int]) -> bool:
        return all(difference > 0 for difference in report_diffs)

    @classmethod
    def is_decreasing(cls, report_diffs: list[int]) -> bool:
        return all(difference < 0 for difference in report_diffs)

    @classmethod
    def is_safe(cls, report: list[int]) -> bool:
        differences = [second - first for first, second in zip(report[:-1], report[1:])]
        if not (cls.is_increasing(differences) or cls.is_decreasing(differences)):
            return False
        return all(1 <= abs(difference) <= 3 for difference in differences)

    def solve(self) -> int:
        return countOf((self.is_safe(report) for report in self.instance.reports), True)
