from operator import countOf

from .problem import ProblemInstance


class PartTwoSolver:
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

    @classmethod
    def is_safe_with_dampener(cls, report: list[int]) -> bool:
        return any(cls.is_safe(report[:i] + report[i+1:]) for i in range(len(report)))

    def solve(self) -> int:
        return countOf((self.is_safe_with_dampener(report) for report in self.instance.reports), True)
