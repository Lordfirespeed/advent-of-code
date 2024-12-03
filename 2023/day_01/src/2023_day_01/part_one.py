from .problem import ProblemInstance


class PartOneSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance
    
    @classmethod
    def recover_calibration_value(cls, line: str) -> int:
        first_digit: str | None = None
        last_digit: str | None = None
        for character in line:
            if not character.isdigit():
                continue
            if first_digit is None:
                first_digit = character
            last_digit = character
        return int(f"{first_digit}{last_digit}")
                
    def solve(self) -> int:
        values = (self.recover_calibration_value(line) for line in self.instance.document)
        return sum(values)
