def getdimensions(string):
    atsymbolindex = string.index("@")
    commaindex = string.index(",")
    colonindex = string.index(":")
    letterxindex = string.index("x")
    distfromleft = int(string[atsymbolindex + 1:commaindex])
    distfromtop = int(string[commaindex + 1:colonindex])
    width = int(string[colonindex + 2:letterxindex])
    height = int(string[letterxindex + 1:])
    dim = {"distfromleft": int(distfromleft),
           "distfromtop": int(distfromtop),
           "width": int(width),
           "height": int(height)}
    return dim

with open("2018day3input.txt") as inputfile:
    inputlines = [line.strip() for line in inputfile.readlines()]

fabric = [[[] for xindex in range(1000)] for yindex in range(1000)]
# fabric should be referenced as fabric[y][x]

for index, claim in enumerate(inputlines):
    listedindex = index + 1
    dimensions = getdimensions(claim)
    for yindex in range(dimensions["distfromtop"], dimensions["distfromtop"] + dimensions["height"]):
        for xindex in range(dimensions["distfromleft"], dimensions["distfromleft"] + dimensions["width"]):
            fabric[yindex][xindex].append(listedindex)

overlaps = [squareinch for yrow in fabric for squareinch in yrow if len(squareinch) > 1]
print(len(overlaps))