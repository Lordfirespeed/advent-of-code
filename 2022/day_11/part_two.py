from typing import Self
from dataclasses import dataclass
from math import prod as product


@dataclass
class Item:
    levels_wrt_monkeys: dict[int, int]

    @classmethod
    def from_original_worry(cls, game: "MonkeyInTheMiddle", original_worry: int):
        levels_wrt_monkeys = {monkey.test_divisible_by: original_worry % monkey.test_divisible_by for index, monkey in game.monkeys.items()}
        return cls(levels_wrt_monkeys)


@dataclass
class Monkey:
    game: "MonkeyInTheMiddle"
    index: int
    items: list[Item] | list[int]
    operation: str
    test_divisible_by: int
    throw_on_true: int
    throw_on_false: int
    number_inspected: int = 0

    @classmethod
    def from_string(cls, game: "MonkeyInTheMiddle", monkey_string: str) -> Self:
        lines = [line.strip() for line in monkey_string.split("\n")]
        index = int(lines[0][7:-1])
        items = [int(item) for item in lines[1][16:].split(", ")]
        operation = lines[2][17:]
        test_divisible_by = int(lines[3][19:])
        throw_on_true = int(lines[4][25:])
        throw_on_false = int(lines[5][26:])

        return cls(game, index, items, operation, test_divisible_by, throw_on_true, throw_on_false)

    def inspect_top_item(self) -> None:
        item: Item = self.items[0]

        for mod_value, worry_wrt_monkey in item.levels_wrt_monkeys.items():
            new_worry_wrt_monkey = eval(self.operation.replace("old", str(worry_wrt_monkey))) % mod_value
            item.levels_wrt_monkeys[mod_value] = new_worry_wrt_monkey

        self.items[0] = item

        self.number_inspected += 1

    def test_top_item(self) -> bool:
        return self.items[0].levels_wrt_monkeys[self.test_divisible_by] == 0


class MonkeyInTheMiddle:
    rounds_to_play = 10000

    def __init__(self, monkey_strings: [str]) -> None:
        monkeys_list = [Monkey.from_string(self, monkey_string) for monkey_string in monkey_strings]
        self.monkeys = {monkey.index: monkey for monkey in monkeys_list}
        self.monkey_indexes = sorted(self.monkeys.keys())
        self.turn_int_worries_into_worries_wrt_monkeys()

    def turn_int_worries_into_worries_wrt_monkeys(self):
        for index, monkey in self.monkeys.items():
            for item_index, item_worry in enumerate(monkey.items):
                monkey.items[item_index] = Item.from_original_worry(self, item_worry)

    @staticmethod
    def apply_relief(monkey: Monkey):
        pass

    def play_monkey_turn(self, monkey_index: int) -> None:
        monkey = self.monkeys[monkey_index]
        while monkey.items:
            monkey.inspect_top_item()
            self.apply_relief(monkey)
            test_result = monkey.test_top_item()

            throw_to_index = monkey.throw_on_true if test_result else monkey.throw_on_false
            throw_to_monkey = self.monkeys[throw_to_index]
            throw_to_monkey.items.append(monkey.items.pop(0))

    def play_round(self) -> None:
        for monkey_index in self.monkey_indexes:
            self.play_monkey_turn(monkey_index)

    def play_game(self) -> None:
        for _ in range(self.rounds_to_play):
            self.play_round()

    def inspection_numbers(self) -> dict[int, int]:
        return {index: monkey.number_inspected for index, monkey in self.monkeys.items()}

    def monkey_business(self) -> int:
        inspection_numbers = self.inspection_numbers().values()
        descending_inspection_numbers = sorted(inspection_numbers, reverse=True)
        return product(descending_inspection_numbers[:2])


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        monkeys_string = input_file.read()
    monkey_strings = monkeys_string.split("\n\n")

    solver = MonkeyInTheMiddle(monkey_strings)
    solver.play_game()
    result = solver.monkey_business()
    print(f"Monkey business level after {solver.rounds_to_play} rounds: {result}")
