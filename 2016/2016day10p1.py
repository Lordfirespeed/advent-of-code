with open("2016day10input.txt") as inputfile:
    inputlist = [line.strip() for line in inputfile.readlines()]
values = [line for line in inputlist if "value" in  line]
gives = [line for line in inputlist if "gives" in line]

bots = {}
outputs = {}

for line in inputlist:
    index = 0
    line += " "
    for index, char in enumerate(line):
        if line[index:index+3] == "bot":
            firstspace = line.index(" ", index+2)
            secondspace = line.index(" ", firstspace+1)
            index = int(line[firstspace:secondspace])
            bots[index] = []
        elif line[index:index+3] == "output":
            firstspace = line.index(" ", index+2)
            secondspace = line.index(" ", firstspace+1)
            index = int(line[firstspace:secondspace])
            outputs[index] = []

for command in values:
    splitstring = command.split(" ")
    value = int(splitstring[1])
    botid = int(splitstring[-1])
    bots[botid].append(value)

rerun = True
execute = list(gives)
while rerun:
    redo = []
    for command in execute:
        splitstring = command.split(" ")
        botgiving = int(splitstring[1])
        if len(bots[botgiving]) == 2:
            lowval = min(bots[botgiving])
            highval = max(bots[botgiving])
            if lowval == 17 and highval == 61:
                print(botgiving)
                rerun = False
                break
            bots[botgiving] = []
            if splitstring[5] == "bot":
                bots[int(splitstring[6])].append(lowval)
            else:
                outputs[int(splitstring[6])].append(lowval)

            if splitstring[-2] == "bot":
                bots[int(splitstring[-1])].append(highval)
            else:
                outputs[int(splitstring[6])].append(lowval)
        else:
            redo.append(command)
    execute = list(redo)
    
