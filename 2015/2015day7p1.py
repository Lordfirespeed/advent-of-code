from numpy import uint16
from collections import defaultdict

with open(r"day7input.txt") as inputfile:
    inputlines = [line.strip() for line in inputfile]

registers = defaultdict(lambda: uint16(0))


def v_or_c(token: str):
    global registers
    if token.isnumeric():
        return uint16(int(token))
    else:
        return registers[token]


def evaluate(instruction: str):
    instruction = instruction.split(" ")
    if len(instruction) == 1:
        return v_or_c(instruction[0])
    elif len(instruction) == 2:
        if instruction[0] == "NOT":
            return ~ v_or_c(instruction[1])
    elif len(instruction) == 3:
        if instruction[1] == "AND":
            return v_or_c(instruction[0]) & v_or_c(instruction[2])
        elif instruction[1] == "OR":
            return v_or_c(instruction[0]) | v_or_c(instruction[2])
        elif instruction[1] == "RSHIFT":
            return v_or_c(instruction[0]) >> v_or_c(instruction[2])
        elif instruction[1] == "LSHIFT":
            return v_or_c(instruction[0]) << v_or_c(instruction[2])
    else:
        print("ACKKK")


for command in inputlines:
    print(command)
    instruction, to_register = command.split(" -> ")
    registers[to_register] = evaluate(instruction)
    print(registers[to_register])

print(f"Value of 'a' register: {registers['a']}")
