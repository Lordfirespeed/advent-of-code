size = 300
grid = [[0 for x in range(size)] for y in range(size)]

serial = 8444

for yindex, yrow in enumerate(grid):
    for xindex, xcol in enumerate(grid[yindex]):
        rack = ((xindex + 1) + 10)
        val = rack * (rack * (yindex + 1) + serial)
        hundreds = int(("000" + str(val))[-3])
        grid[yindex][xindex] = hundreds - 5

squaresgrid = [[0 for x in range(size-2)] for y in range(size-2)]
for yindex, yrow in enumerate(grid[:-2]):
    for xindex, xcol in enumerate(grid[yindex][:-2]):
        square = sum([grid[yindex+y][xindex+x] for y in range(3) for x in range(3)])
        squaresgrid[yindex][xindex] = square

maximum = max([(max([obj[::-1] for obj in enumerate(row)]) + tuple([yindex])) for yindex, row in enumerate(squaresgrid)])
print(f"Maximum: {maximum[0]}, at ({maximum[1]+1}, {maximum[2]+1})")
