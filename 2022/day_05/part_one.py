from __future__ import annotations
import re
from dataclasses import dataclass
from typing import ClassVar


class CrateStacks:
    def __init__(self, stack_string: str) -> None:
        stack_lines = stack_string.split("\n")
        self.stack_indexes = [int(index_string) for index_string in batched_string(stack_lines[-1], 4)]
        self.stacks: {int, [str]} = {index: [] for index in self.stack_indexes}
        self._populate_stacks(stack_lines[:-1])

    def __getitem__(self, index) -> [str]:
        return self.stacks[index]

    def _populate_stacks(self, stack_lines: [str]) -> None:
        for stack_line in reversed(stack_lines):
            for stack_index, stack_element in zip(self.stack_indexes, batched_string(stack_line, 4)):
                if not stack_element.strip():
                    continue
                crate_name = stack_element[1]
                self.stacks[stack_index].append(crate_name)

    def top_of_each_stack(self) -> str:
        return "".join([self.stacks[index][-1] for index in self.stack_indexes])


class Crane:
    @dataclass
    class Instruction:
        quantity: int
        from_index: int
        to_index: int

        pattern: ClassVar[re.Pattern] = re.compile(r"move (\d+) from (\d+) to (\d+)")

        @classmethod
        def from_string(cls, instruction_string: str) -> Crane.Instruction:
            match = re.match(cls.pattern, instruction_string)
            if not match:
                raise ValueError

            quantity, from_index, to_index = map(int, match.groups())

            return cls(quantity, from_index, to_index)

    def __init__(self, stacks: CrateStacks, instructions: [str]) -> None:
        self.stacks = stacks
        self.instructions = instructions.split("\n")

    def move_one_box(self, from_stack_index: int, to_stack_index: int) -> None:
        box = self.stacks[from_stack_index].pop()
        self.stacks[to_stack_index].append(box)

    def execute_instruction(self, instruction: str) -> None:
        instruction = self.Instruction.from_string(instruction)
        for _ in range(instruction.quantity):
            self.move_one_box(instruction.from_index, instruction.to_index)

    def execute_instructions(self) -> None:
        for instruction in self.instructions:
            self.execute_instruction(instruction)


def batched_string(a: str, batch_size: 4) -> [str]:
    for index in range(0, len(a), batch_size):
        yield a[index:index + batch_size]


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        crates, instructions = input_file.read().split("\n\n")

    stacks = CrateStacks(crates)
    solver = Crane(stacks, instructions)
    solver.execute_instructions()
    result = stacks.top_of_each_stack()
    print(f"Boxes at top of stacks after instructions complete: {result}")
