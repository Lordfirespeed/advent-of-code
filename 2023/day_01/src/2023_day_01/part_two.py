from .problem import ProblemInstance


class PartTwoSolver:
    spelled_digits = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    @classmethod
    def recover_calibration_value(cls, line: str) -> int:
        first_digit: int | None = None
        last_digit: int | None = None
        
        def saw_digit(digit: int) -> None:
            nonlocal first_digit
            nonlocal last_digit

            if first_digit is None:
                first_digit = digit
            last_digit = digit
        
        cursor = 0
        while cursor < len(line):
            for spelled_digit, spelled_digit_value in cls.spelled_digits.items():
                if not line[cursor:].startswith(spelled_digit):
                    continue
                
                saw_digit(spelled_digit_value)
                cursor += 1
                break
            else:
                character = line[cursor]
                if character.isdigit():
                    saw_digit(int(character))
                    cursor += 1
                    continue
    
                cursor += 1
        return int(f"{first_digit}{last_digit}")

    def solve(self) -> int:
        values = (self.recover_calibration_value(line) for line in self.instance.document)
        return sum(values)
