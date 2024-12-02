from collections import defaultdict

from .problem import ProblemInstance


class PartTwoSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    def solve(self) -> int:
        right_list_counts = defaultdict(int)
        for value in self.instance.right_list:
            right_list_counts[value] += 1

        similarity_score = 0
        for value in self.instance.left_list:
            similarity_score += value * right_list_counts[value]

        return similarity_score
