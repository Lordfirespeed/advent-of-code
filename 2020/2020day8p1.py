with open(r"Input\2020day8.txt") as inputfile:
    input_tokens = [line.strip().split(" ") for line in inputfile.readlines()]

accumulator = 0
current_instruction_index = 0
executed_instruction_indices = []
while current_instruction_index not in executed_instruction_indices:
    operator, operand = input_tokens[current_instruction_index]
    executed_instruction_indices.append(current_instruction_index)
    if operator == "jmp":
        current_instruction_index += int(operand)
    else:
        if operator == "nop":
            pass
        elif operator == "acc":
            accumulator += int(operand)
        current_instruction_index += 1

print(f"Accumulator value before repeat loop: {accumulator}")
