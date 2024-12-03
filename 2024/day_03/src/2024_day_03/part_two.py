import re

from .problem import ProblemInstance


class PartTwoSolver:
    mul_instruction_pattern = re.compile('mul\((?P<left>\d{1,3}),(?P<right>\d{1,3})\)')
    do_instruction_pattern = re.compile('do\(\)')
    do_not_instruction_pattern = re.compile('don\'t\(\)')

    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    def solve(self) -> int:
        cursor = 0
        result = 0
        mul_instructions_enabled = True
        while cursor < len(self.instance.memory):
            do_instruction_match = self.do_instruction_pattern.match(self.instance.memory, cursor)
            if do_instruction_match is not None:
                cursor = do_instruction_match.end()
                mul_instructions_enabled = True
                continue
            
            do_not_instruction_match = self.do_not_instruction_pattern.match(self.instance.memory, cursor)
            if do_not_instruction_match is not None:
                cursor = do_not_instruction_match.end()
                mul_instructions_enabled = False
                continue
            
            mul_instruction_match = self.mul_instruction_pattern.match(self.instance.memory, cursor)
            if mul_instruction_match is not None:
                cursor = mul_instruction_match.end()
                if mul_instructions_enabled: result += int(mul_instruction_match.group("left")) * int(mul_instruction_match.group("right"))
                continue
            
            cursor += 1
                
        return result
