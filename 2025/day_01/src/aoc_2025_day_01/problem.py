import dataclasses
import enum
from typing import Self

from problem_instance_abc import ProblemInstanceABC


@enum.verify(enum.UNIQUE)
class TurnDirection(enum.StrEnum):
    Left = "L"
    Right = "R"


@dataclasses.dataclass
class Turn:
    direction: TurnDirection
    distance: int

    @classmethod
    def from_raw(cls, raw: str) -> Self:
        direction = TurnDirection(raw[0])
        distance = int(raw[1:])
        return cls(direction, distance)


class ProblemInstance(ProblemInstanceABC):
    turns: list[Turn]

    def parse_plaintext(self) -> None:
        lines = self.input_plaintext.splitlines()
        self.turns = [Turn.from_raw(raw_turn) for raw_turn in lines]
