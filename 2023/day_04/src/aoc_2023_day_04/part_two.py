import functools
from operator import countOf

from .problem import Card, ProblemInstance


class PartTwoSolver:
    won_cards: list[Card]

    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance
        self.cards_by_id = {card.card_id: card for card in self.instance.cards}
        self.reset()

    def reset(self) -> None:
        self.won_cards = self.instance.cards.copy()

    @classmethod
    def matching_count(cls, card: Card) -> int:
        return countOf((held in card.winning_numbers for held in card.held_numbers), True)

    @functools.cache
    def cards_won_by(self, card: Card) -> list[Card]:
        won_card_ids = range(card.card_id + 1, card.card_id + 1 + self.matching_count(card))
        return [self.cards_by_id[card_id] for card_id in won_card_ids]

    def solve(self) -> int:
        cursor = 0
        while cursor < len(self.won_cards):
            card = self.won_cards[cursor]
            cursor += 1
            self.won_cards[cursor:cursor] = self.cards_won_by(card)

        return len(self.won_cards)
