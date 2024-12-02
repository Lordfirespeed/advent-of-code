class Solution:
    def __init__(self, input_lines: [str]) -> None:
        self.string_commands = input_lines
        self.x_register = 1
        self.current_instruction = None
        self.instruction_index = 0
        self.cycle_number = 0
        self.signal_strengths = []

    def noop(self):
        yield  # start of 1st cycle
        return  # end of 1st cycle

    def addx(self, value):
        yield  # start of 1st cycle
        yield  # end of 1st cycle
        self.x_register += value
        return  # end of 2nd cycle

    def instruction_from_string(self, instruction_string):
        if instruction_string.startswith("noop"):
            return self.noop()
        if instruction_string.startswith("addx"):
            _, value_string = instruction_string.split(" ")
            return self.addx(int(value_string))
        raise NotImplementedError

    def instruction_at_index(self, index):
        return self.instruction_from_string(self.string_commands[index])

    def instruction_at_current_index(self):
        return self.instruction_at_index(self.instruction_index)

    def execute_cycle(self):
        self.current_instruction = self.instruction_at_current_index()
        next(self.current_instruction)
        while True:
            self.cycle_number += 1
            try:
                next(self.current_instruction)
            except StopIteration:
                self.instruction_index += 1
                if self.instruction_index >= len(self.string_commands):
                    return
                self.current_instruction = self.instruction_at_current_index()
                next(self.current_instruction)
            yield

    def record_current_signal_strength(self):
        signal_strength = self.x_register * (self.cycle_number + 1)
        self.signal_strengths.append(signal_strength)

    def run_program(self):
        cycle_executor = self.execute_cycle()
        while True:
            if self.cycle_number >= 19 and (self.cycle_number - 19) % 40 == 0:
                self.record_current_signal_strength()

            if self.cycle_number > 220:
                break

            try:
                next(cycle_executor)
            except StopIteration:
                break

    def signal_strength_sum(self) -> int:
        return sum(self.signal_strengths)


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        input_lines = [line.strip() for line in input_file.readlines()]

    solver = Solution(input_lines)
    solver.run_program()
    result = solver.signal_strength_sum()
    print(f"Signal strength sums: {result}")
