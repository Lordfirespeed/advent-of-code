
from itertools import product

with open(r"Input\2020day14.txt") as inputfile:
    inputlines = [line.strip() for line in inputfile.readlines()]


class Unsigned_36Bit:
    def __init__(self, number):
        self.binary = self.correct_length(bin(number).replace("b", ""))

    def __int__(self):
        return int(self.binary, 2)

    @staticmethod
    def correct_length(binary):
        return ("0" * (36 - len(binary)) + binary)[-36:]

    def mask(self, mask):
        self.binary = self.correct_length("".join([oc if oc != "0" else bc for oc, bc in zip(mask, self.binary)]))


tokens = [line.split(" = ") for line in inputlines]

mask = ""
memory = {}

for setting, value in tokens:
    if setting == "mask":
        mask = value
    else:
        to_index_unmasked = Unsigned_36Bit(int(setting[4:-1]))
        to_index_unmasked.mask(mask)
        to_index = to_index_unmasked.binary
        for possible in product(("0", "1"), repeat=to_index.count("X")):
            curr_to_index = to_index
            for num in possible:
                curr_to_index = curr_to_index.replace("X", num, 1)
            memory[curr_to_index] = int(value)

print(f"Sum of all values left in memory: {sum(memory.values())}")
