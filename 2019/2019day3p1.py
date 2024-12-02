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
        #print(newpos)
        ychange = -1 if newpos[0] < curr[0] else 1
        xchange = -1 if newpos[1] < curr[1] else 1
        points += [(y, x) for y in range(curr[0], newpos[0]+ychange, ychange) for x in range(curr[1], newpos[1]+xchange, xchange)]
        curr = newpos
    return set(points)


intersects = set.intersection(getlinepoints(a), getlinepoints(b))
intersects.remove((0, 0))
dists = [abs(y) + abs(x) for y, x in intersects]
print(min(dists))
