from operator import countOf

from .problem import Card, ProblemInstance


class PartOneSolver:
    total_worth: int

    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance
        self.reset()

    def reset(self) -> None:
        self.total_worth = 0

    @classmethod
    def card_worth(cls, card: Card) -> int:
        matching_count = countOf((held in card.winning_numbers for held in card.held_numbers), True)
        if matching_count == 0:
            return 0
        return 2 ** (matching_count - 1)

    def solve(self) -> int:
        return sum(self.card_worth(card) for card in self.instance.cards)
