with open(r"Input\2021day2.txt") as inputFile:
    inputLines = [line.strip() for line in inputFile.readlines()]

commands = [line.split(" ") for line in inputLines]
horizontal, depth, aim = 0, 0, 0

for command, value in commands:
    if command == "forward":
        horizontal += int(value)
        depth += aim * int(value)
    elif command == "down":
        aim += int(value)
    elif command == "up":
        aim -= int(value)

answer = horizontal * depth
print(f"The answer is {answer}")
