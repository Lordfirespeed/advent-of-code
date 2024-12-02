size = 300
grid = [[0 for x in range(size)] for y in range(size)]

serial = 8444

for yindex, yrow in enumerate(grid):
    for xindex, xcol in enumerate(grid[yindex]):
        rack = ((xindex + 1) + 10)
        val = rack * (rack * (yindex + 1) + serial)
        hundreds = int(("000" + str(val))[-3])
        grid[yindex][xindex] = hundreds - 5

squares = [(grid.copy(), 1)]
for squaresize in range(2, 301):
    squaresgrid = [[0 for x in range(size-(squaresize - 1))] for y in range(size-(squaresize - 1))]
    for yindex, yrow in enumerate(grid[:-(squaresize - 1)]):
        for xindex, xcol in enumerate(grid[yindex][:-(squaresize - 1)]):
            square = sum([grid[yindex+y][xindex+x] for y in range(squaresize) for x in range(squaresize)])
            squaresgrid[yindex][xindex] = square
    squares.append((squaresgrid.copy(), squaresize))

maximum = max([(max([obj[::-1] for obj in enumerate(row)]) + tuple([yindex])) for yindex, row in enumerate(squaresgrid)])
print(f"Maximum: {maximum[0]}, at ({maximum[1]+1}, {maximum[2]+1})")
