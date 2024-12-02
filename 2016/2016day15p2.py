with open("2016day15p2input.txt") as inputfile:
    inputlines = [line.strip() for line in inputfile.readlines()]

inputdata = []
for index, line in enumerate(inputlines):
    posindex = line.index("has ") + 4
    positions = line[posindex:line.index(" ", posindex)]
    posindex = line.index("position ") + 9
    currentposition = line[posindex:line.index(".", posindex)]
    inputdata.append([int(positions), int(currentposition)])

def drop(discs, droptime):
    positions = [(disc[1] + droptime + discindex + 1) % disc[0] for discindex, disc in enumerate(discs)]
    if len(set(positions)) == 1 and positions[0] == 0:
        return True
    else:
        return False

time = 0
solved = False
while not solved:
    if drop(inputdata, time):
        print("Drop successful at " + str(time) + ".")
        solved = True
    else:
        time += 1