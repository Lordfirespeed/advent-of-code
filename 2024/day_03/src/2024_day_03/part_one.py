import re

from .problem import ProblemInstance


class PartOneSolver:
    mul_instruction_pattern = re.compile('mul\((?P<left>\d{1,3}),(?P<right>\d{1,3})\)')
    
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    def solve(self) -> int:
        matches = self.mul_instruction_pattern.finditer(self.instance.memory)
        return sum(int(match.group("left")) * int(match.group("right")) for match in matches)
