from .problem import ProblemInstance


class PartOneSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    def solve(self) -> int:
        ordered_left_list = sorted(self.instance.left_list)
        ordered_right_list = sorted(self.instance.right_list)
        differences = [
            abs(left_value - right_value) for left_value, right_value in zip(ordered_left_list, ordered_right_list)
        ]
        return sum(differences)
