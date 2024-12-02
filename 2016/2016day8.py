gridx = 50
gridy = 6
grid = [["0" for x in range(gridx)] for y in range(gridy)]
# grid coords are in format grid[y][x]

commands = {
    "rect ":"rect(arga, argb)",
    "rotate row y=":"rotaterow(arga, argb)",
    "rotate column x=":"rotatecolumn(arga, argb)"
    }

with open("2016day8input.txt") as inputfile:
    inputlist = [line.strip().replace(" by ", "x") for line in inputfile.readlines()]

def rect(a, b):
    # a wide, b tall - top left corner ON
    for y in range(b):
        for x in range(a):
            grid[y][x] = "X"

def rotaterow(a, b):
    # rotate row index a RIGHT by b pixels
    newline = list(enumerate(grid[a]))
    newline = [[(index+b)%len(newline), value] for index, value in newline]
    for value in newline:
        grid[a][value[0]] = value[1]

def rotatecolumn(a, b):
    # rotate column index a DOWN by b pixels
    newline = list(enumerate([line[a] for line in grid]))
    newline = [[(index+b)%len(newline), value] for index, value in newline]
    for value in newline:
        grid[value[0]][a] = value[1]

def outgrid():
    totalon = 0
    for line in grid:
        print("".join(line).replace("0", " ").replace("X", u"\u25A0"))
        totalon += line.count("X")
    print(totalon)

for line in inputlist:
    for command in commands:
        if command in line:
            args = line.replace(command, "")
            arga, argb = list(map(int, args.split("x")))
            exec(commands[command])


