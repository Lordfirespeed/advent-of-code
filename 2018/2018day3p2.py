def getdimensions(string):
    atsymbolindex: int = string.index("@")
    commaindex: int = string.index(",")
    colonindex: int = string.index(":")
    letterxindex: int = string.index("x")
    distfromleft = int(string[atsymbolindex + 1:commaindex])
    distfromtop = int(string[commaindex + 1:colonindex])
    width = int(string[colonindex + 2:letterxindex])
    height = int(string[letterxindex + 1:])
    dictdimensions = {"distfromleft": int(distfromleft),
                      "distfromtop": int(distfromtop),
                      "width": int(width),
                      "height": int(height)}
    return dictdimensions


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
overlappingindexes = set([claimindex for squareinch in overlaps for claimindex in squareinch])
allindexes = set(range(1, len(inputlines)+1))
safeindex = list((allindexes - overlappingindexes))[0]
print("ID of claim with no overlaps: " + str(safeindex))
