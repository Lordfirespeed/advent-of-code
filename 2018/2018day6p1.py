def manhdist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def compute(coords, addrange=0):
    xvals, yvals = zip(*coords)
    minx, maxx, miny, maxy = min(xvals) - addrange, max(xvals) + addrange, min(yvals) - addrange, max(yvals) + addrange
    grid = dict([(y, dict([(x, {}) for x in range(minx, maxx+1)])) for y in range(miny, maxy+1)])

    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            if [x, y] in coords:
                grid[y][x][0] = [coords.index([x, y])]
            else:
                for index, point in enumerate(coords):
                    dist = manhdist((x, y), point)
                    try:
                        grid[y][x][dist]
                    except KeyError:
                        grid[y][x][dist] = []
                    grid[y][x][dist].append(index)

    totals = [0 for _ in coords]

    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            if len(grid[y][x][(minindex := min(grid[y][x].keys()))]) == 1:
                totals[grid[y][x][minindex][0]] += 1

    return totals


with open("2018day6input.txt") as inputfile:
    lines = [line.strip() for line in inputfile.readlines()]
    points = [[int(n) for n in line.split(", ")] for line in lines]

totalsA = compute(points)
totalsB = compute(points, 1)

totals = [totalA if totalA == totalB else 0 for totalA, totalB in zip(totalsA, totalsB)]

print(max(totals))
