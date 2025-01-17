from dataclasses import dataclass
from typing import Self

from problem_instance_abc import ProblemInstanceABC


@dataclass(frozen=True)
class CalibrationEquation:
    result: int
    operands: tuple[int, ...]

    @classmethod
    def from_plaintext(cls, plaintext: str) -> Self:
        parts = plaintext.split(": ")
        assert len(parts) == 2
        result_str, operands_str = parts
        result = int(result_str)
        operands = tuple(int(operand) for operand in operands_str.split())
        return cls(result, operands)


class ProblemInstance(ProblemInstanceABC):
    equations: tuple[CalibrationEquation, ...]

    def parse_plaintext(self) -> None:
        self.equations = tuple(CalibrationEquation.from_plaintext(line) for line in self.input_plaintext.splitlines())
