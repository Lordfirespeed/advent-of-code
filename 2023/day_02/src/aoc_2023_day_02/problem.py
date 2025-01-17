from dataclasses import dataclass
from typing import Self

from problem_instance_abc import ProblemInstanceABC


@dataclass(frozen=True)
class Handful:
    red: int
    green: int
    blue: int

    @classmethod
    def from_string(cls, handful_string: str) -> Self:
        colour_counts = {"red": 0, "green": 0, "blue": 0}
        for clause in handful_string.split(", "):
            count, colour = clause.split(" ")
            assert count.isdigit()
            assert colour in colour_counts
            colour_counts[colour] += int(count)
        return cls(**colour_counts)


@dataclass
class Game:
    game_id: int
    history: list[Handful]

    @classmethod
    def from_string(cls, game_string: str) -> Self:
        assert game_string.startswith("Game ")
        colon_index = game_string.index(":")
        game_id = int(game_string[5:colon_index])
        handful_strings = game_string[colon_index + 2:].split("; ")
        handfuls = [Handful.from_string(handful_string) for handful_string in handful_strings]
        return cls(game_id, handfuls)


class ProblemInstance(ProblemInstanceABC):
    games: list[Game]

    def parse_plaintext(self) -> None:
        game_strings = self.input_plaintext.splitlines()
        self.games = [Game.from_string(game_string) for game_string in game_strings]
