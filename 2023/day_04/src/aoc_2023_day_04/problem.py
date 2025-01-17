from dataclasses import dataclass
from typing import Self

from problem_instance_abc import ProblemInstanceABC


@dataclass
class Card:
    card_id: int
    winning_numbers: list[int]
    held_numbers: list[int]

    @classmethod
    def from_string(cls, card_string: str) -> Self:
        assert card_string.startswith("Card ")
        colon_index = card_string.index(":")
        card_id = int(card_string[5:colon_index])
        rest = card_string[colon_index + 1:].lstrip()
        winning_numbers_string, held_numbers_string = rest.split(" | ")
        winning_numbers = [int(number_string) for number_string in winning_numbers_string.split()]
        held_numbers = [int(number_string) for number_string in held_numbers_string.split()]
        return cls(card_id, winning_numbers, held_numbers)

    def __eq__(self, other):
        return self is other  # by-reference equality

    def __hash__(self):
        return id(self)  # by-reference equality


class ProblemInstance(ProblemInstanceABC):
    cards: list[Card]

    def parse_plaintext(self) -> None:
        self.cards = [Card.from_string(line) for line in self.input_plaintext.splitlines()]
