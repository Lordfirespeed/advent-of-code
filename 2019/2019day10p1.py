from fractions import Fraction
from math import atan, degrees


def findasteroids(x, y):
    global grid
    canSee = set()
    for checky, row in enumerate(grid):
        for checkx, position in enumerate(row):
            if position == "#":  # if the square is an asteroid
                if x == checkx and y == checky:
                    pass
                else:
                    diffx, diffy = checkx - x, checky - y
                    diffxsign, diffysign = diffx >= 0, diffy >= 0
                    if diffx == 0:
                        angle = 0 if diffysign else 180
                    elif diffy == 0:
                        angle = 90 if diffxsign else 270
                    else:
                        angle = degrees(atan(Fraction(abs(diffx), abs(diffy))))
                        if (not diffxsign) and (not diffysign):
                            angle += 180
                        elif not diffxsign:
                            angle = 360 - angle
                        elif not diffysign:
                            angle += 90
                    canSee.add(angle)
    return canSee


with open("Input/2019day10input.txt") as inputfile:
    grid = [list(line.strip()) for line in inputfile.readlines()]

numasteroids = {}
for y, row in enumerate(grid):
    for x, position in enumerate(row):
        if position == "#":  # if the square is an asteroid
            numasteroids[(x, y)] = findasteroids(x, y)

print(max([len(canSee) for canSee in numasteroids.values()]))

