from typing import NamedTuple, Self

from problem_instance_abc import ProblemInstanceABC


class PageOrderingRule(NamedTuple):
    first: int
    second: int

    @classmethod
    def from_string(cls, string: str) -> Self:
        first_string, second_string = string.split("|")
        return cls(first=int(first_string), second=int(second_string))


type Update = list[int]  # an Update is a list of pages to produce


class ProblemInstance(ProblemInstanceABC):
    page_ordering_rules: list[PageOrderingRule]
    updates: list[Update]

    def parse_plaintext(self) -> None:
        page_ordering_rules_plaintext, updates_plaintext = self.input_plaintext.split("\n\n")
        page_ordering_rule_strings = page_ordering_rules_plaintext.splitlines()
        self.page_ordering_rules = [PageOrderingRule.from_string(string) for string in page_ordering_rule_strings]
        self.updates = [[int(page_no) for page_no in update.split(",")] for update in updates_plaintext.splitlines()]
