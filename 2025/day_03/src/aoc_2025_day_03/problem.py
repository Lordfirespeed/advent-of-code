from collections import UserList
from typing import NewType

from problem_instance_abc import ProblemInstanceABC


BatteryJoltage = NewType("BatteryJoltage", int)
class BatteryBank(UserList[BatteryJoltage]):
    pass


class ProblemInstance(ProblemInstanceABC):
    banks: list[BatteryBank]

    def parse_plaintext(self) -> None:
        lines = self.input_plaintext.splitlines()
        self.banks = [BatteryBank([BatteryJoltage(int(joltage)) for joltage in raw_bank]) for raw_bank in lines]

