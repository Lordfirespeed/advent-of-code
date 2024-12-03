from .problem import ProblemInstance


class PartTwoSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    def solve(self) -> int:
        return len(self.instance.input_plaintext)
