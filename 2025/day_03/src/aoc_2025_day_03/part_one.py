from math import inf

from .problem import ProblemInstance, BatteryBank, BatteryJoltage


class PartOneSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    def max_joltage(self, bank: BatteryBank) -> BatteryJoltage:
        superior_joltage_sequence = BatteryBank(bank)
        for index in reversed(range(len(bank) - 1)):
            if superior_joltage_sequence[index + 1] <= superior_joltage_sequence[index]: continue
            superior_joltage_sequence[index] = superior_joltage_sequence[index + 1]

        max_joltage = -inf
        for first_digit_index in range(len(bank) - 1):
            first_digit = bank[first_digit_index]
            second_digit = superior_joltage_sequence[first_digit_index + 1]
            candidate_joltage = int(f"{first_digit}{second_digit}")
            if candidate_joltage <= max_joltage: continue
            max_joltage = candidate_joltage
        return BatteryJoltage(max_joltage)

    def solve(self) -> int:
        total_output_joltage = 0
        for bank in self.instance.banks:
            bank_output = self.max_joltage(bank)
            total_output_joltage += bank_output
        return total_output_joltage
