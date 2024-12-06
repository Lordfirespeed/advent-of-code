import graphlib
from graphlib import TopologicalSorter
from typing import Iterable, Sequence

from .problem import PageOrderingRule, ProblemInstance


class PartOneSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    @classmethod
    def build_graph(cls, rules: Iterable[PageOrderingRule]) -> dict[int, set[int]]:
        graph: dict[int, set[int]] = {}
        for update in rules:
            if update.second not in graph:
                graph[update.second] = set()
            graph[update.second].add(update.first)
        return graph

    @classmethod
    def page_order(cls, rules: Iterable[PageOrderingRule], pages: Sequence[int]) -> tuple[int, ...]:
        graph = cls.build_graph(rule for rule in rules if rule.first in pages and rule.second in pages)
        try:
            ts = TopologicalSorter(graph)
            return tuple(ts.static_order())
        except graphlib.CycleError:
            return tuple()

    @classmethod
    def is_correctly_ordered(cls, update: Sequence[int], order: Sequence[int]) -> bool:
        order_pos = 0
        for page in update:
            try:
                order_pos = order.index(page, order_pos) + 1
            except ValueError:
                return False
        return True

    def correctly_ordered_updates(self) -> Iterable[Sequence[int]]:
        for update in self.instance.updates:
            order = self.page_order(self.instance.page_ordering_rules, update)
            if not self.is_correctly_ordered(update, order):
                continue
            yield update

    @classmethod
    def middle_page_number(cls, update: Sequence[int]) -> int:
        middle_index, remainder = divmod(len(update), 2)
        assert remainder == 1  # if the update length is even, the 'middle page' is ill-defined, so something is wrong
        return update[middle_index]

    def solve(self) -> int:
        return sum(self.middle_page_number(update) for update in self.correctly_ordered_updates())
