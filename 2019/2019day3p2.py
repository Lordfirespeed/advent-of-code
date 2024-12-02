with open("Input/2019day3input.txt") as inputfile:
    lineinfo = [line.strip().split(",") for line in inputfile.readlines()]
    a, b = lineinfo


def getlinepoints(line):
    curr = [0, 0]
    points = []
    for move in line:
        newpos = curr.copy()
        if move[0] == "U":
            newpos[0] -= int(move[1:])
        elif move[0] == "D":
            newpos[0] += int(move[1:])
        elif move[0] == "L":
            newpos[1] -= int(move[1:])
        else:
            newpos[1] += int(move[1:])
        ychange = -1 if newpos[0] < curr[0] else 1
        xchange = -1 if newpos[1] < curr[1] else 1
        toadd = [(y, x) for y in range(curr[0], newpos[0]+ychange, ychange) for x in range(curr[1], newpos[1]+xchange, xchange)]
        toadd.remove(tuple(curr))
        points += toadd
        curr = newpos
    return list(enumerate(points, 1))


apoints, bpoints = getlinepoints(a), getlinepoints(b)
alocs, blocs = [loc[1] for loc in apoints], [loc[1] for loc in bpoints]
alocset, blocset = set(alocs), set(blocs)
intersects = set.intersection(alocset, blocset)

dists = []
for point in list(intersects):
    aindex, bindex = alocs.index(point), blocs.index(point)
    dist = apoints[aindex][0] + bpoints[bindex][0]
    dists.append(dist)

print(min(dists))
