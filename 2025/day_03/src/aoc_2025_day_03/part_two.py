from .problem import ProblemInstance, BatteryBank, BatteryJoltage


class PartTwoSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    def max_joltage(self, bank: BatteryBank) -> BatteryJoltage:
        selection = bank[-12:]

        for index in reversed(range(len(bank) - 12)):
            digit = bank[index]
            for compare_index in range(len(selection)):
                compare_digit = selection[compare_index]
                if compare_digit > digit: break
                selection[compare_index] = digit
                digit = compare_digit

        selection_joltage = int("".join((str(joltage) for joltage in selection)))

        return BatteryJoltage(selection_joltage)

    def solve(self) -> int:
        total_output_joltage = 0
        for bank in self.instance.banks:
            bank_output = self.max_joltage(bank)
            total_output_joltage += bank_output
        return total_output_joltage
