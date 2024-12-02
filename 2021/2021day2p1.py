with open(r"Input\2021day2.txt") as inputFile:
    inputLines = [line.strip() for line in inputFile.readlines()]

commands = [line.split(" ") for line in inputLines]
horizontal, depth = 0, 0

for command, value in commands:
    if command == "forward":
        horizontal += int(value)
    elif command == "down":
        depth += int(value)
    elif command == "up":
        depth -= int(value)

answer = horizontal * depth
print(f"The answer is {answer}")
