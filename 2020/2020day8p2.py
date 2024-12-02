with open(r"Input\2020day8.txt") as inputfile:
    input_tokens = [line.strip().split(" ") for line in inputfile.readlines()]


def run_program(instr):
    accumulator = 0
    current_instruction_index = 0
    executed_instruction_indices = []
    try:
        while current_instruction_index not in executed_instruction_indices:
            operator, operand = instr[current_instruction_index]
            executed_instruction_indices.append(current_instruction_index)
            if operator == "jmp":
                current_instruction_index += int(operand)
            else:
                if operator == "nop":
                    pass
                elif operator == "acc":
                    accumulator += int(operand)
                current_instruction_index += 1
    except IndexError:
        if len(instr) - 1 in executed_instruction_indices:
            return accumulator

    return None


for index, instruction in enumerate(input_tokens):
    if instruction[0] == "nop" or instruction[0] == "jmp":
        try_instr = input_tokens.copy()
        try_instr[index] = [{"nop": "jmp", "jmp": "nop"}[instruction[0]], instruction[1]]
        result = run_program(try_instr)
        if result:
            print(f"Accumulator value after successful execution: {result}")
            break
