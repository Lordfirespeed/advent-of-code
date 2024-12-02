def manhdist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def compute(coords, addrange=0):
    xvals, yvals = zip(*coords)
    minx, maxx, miny, maxy = min(xvals) - addrange, max(xvals) + addrange, min(yvals) - addrange, max(yvals) + addrange
    grid = dict([(y, dict([(x, {}) for x in range(minx, maxx+1)])) for y in range(miny, maxy+1)])

    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            for index, point in enumerate(coords):
                dist = manhdist((x, y), point)
                try:
                    grid[y][x][dist]
                except KeyError:
                    grid[y][x][dist] = []
                grid[y][x][dist].append(index)

    totals = dict([(y, {}) for y in range(miny, maxy+1)])

    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            total = 0
            for dist in grid[y][x].keys():
                total += dist * len(grid[y][x][dist])
            totals[y][x] = total

    return totals


with open("2018day6input.txt") as inputfile:
    lines = [line.strip() for line in inputfile.readlines()]
    points = [[int(n) for n in line.split(", ")] for line in lines]

vals = compute(points)
totals = [vals[y][x] for y in vals.keys() for x in vals[y].keys()]

print(len([t for t in totals if t < 10000]))
