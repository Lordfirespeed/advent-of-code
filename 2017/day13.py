with open("day13input.txt") as inputfile:
    walldict = {}
    highestdepth = 0
    for index, line in enumerate(inputfile.readlines(), 1):
        line = line.rstrip()
        depth, wallheight = line.split(": ")
        depth, wallheight = int(depth), int(wallheight)
        walldict[depth] = wallheight
        if depth > highestdepth:
            highestdepth = depth

def partone():
    severity = 0
    for depth in range((highestdepth + 1)):
        try:
            wallheight = walldict[depth]
            if not (depth % (2 * (wallheight - 1))):
                severity += depth * wallheight
        except KeyError:
            wallnotfound = True

    print(severity)

def parttwo():
    solution = False
    startat = 1
    while not solution:
        solution = True
        for depth in range(startat, (startat + highestdepth + 1)):
            try:
                wallheight = (walldict[depth - startat])
                if not (depth % (2 * (wallheight - 1))):
                    solution = False
                    break
            except KeyError:
                wallnotfound = True
        if solution:
            print(startat)
            break

        startat += 1
    
