with open("day6input.txt") as inputfile:
    inputlines = [line.strip() for line in inputfile.readlines()]


def format(command):
    if "turn" in command:
        command = command.replace(" ", "", 1)
    command = command.replace(" through ", "], [", 1)
    command = command.replace(" ", "([", 1)
    command += "])"
    return command


commands = list(map(format, inputlines))

grid = [[0 for x in range(1000)] for y in range(1000)]
# reference grid in format grid[y][x]
# grid functions:


def turnon(location1, location2):
    for coords in [[x, y] for x in range(location1[0], location2[0]+1) for y in range(location1[1], location2[1]+1)]:
        grid[coords[1]][coords[0]] += 1


def turnoff(location1, location2):
    for coords in [[x, y] for x in range(location1[0], location2[0]+1) for y in range(location1[1], location2[1]+1)]:
        grid[coords[1]][coords[0]] -= 1
        if grid[coords[1]][coords[0]] < 0:
            grid[coords[1]][coords[0]] = 0


def toggle(location1, location2):
    for coords in [[x, y] for x in range(location1[0], location2[0]+1) for y in range(location1[1], location2[1]+1)]:
        grid[coords[1]][coords[0]] += 2


for index, command in enumerate(commands):
    exec(command)
    print("Executed " + str(index))

print(sum([integer for xline in grid for integer in xline]))
