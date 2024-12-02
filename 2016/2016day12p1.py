with open("2016day12input.txt") as inputfile:
    inputlist = [line.strip() for line in inputfile]
inputlist = [command.split(" ") for command in inputlist]
inputlist = [([command[0]] + [("'" + substring + "'") for substring in command[1:]]) for command in inputlist]
inputlist = [(command[0] + "(" + ", ".join(command[1:]) + ")") for command in inputlist]

def cpy(x, y):
    if x.isdigit():
        registers[y] = int(x)
    else:
        registers[y] = int(registers[x])

def inc(x):
    registers[x] += 1

def dec(x):
    registers[x] -= 1

def jnz(x, y):
    global cmdindex
    if x.isdigit():
        x = int(x)
    else:
        try:
            x = int(registers[x])
        except KeyError:
            registers[x] = 0
            x = 0
    if x != 0:
        cmdindex += int(y) - 1

registers = {}
cmdindex = 0

while cmdindex < len(inputlist):
    exec(inputlist[cmdindex])
    cmdindex += 1

print(registers)