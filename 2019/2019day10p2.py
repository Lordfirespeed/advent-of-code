from fractions import Fraction
from math import atan, degrees


def findasteroids(x, y):
    global grid
    canSee = {}
    for checky, row in enumerate(grid):
        for checkx, position in enumerate(row):
            if position == "#":  # if the square is an asteroid
                if x == checkx and y == checky:
                    pass
                else:
                    diffx, diffy = checkx - x, -(checky - y)
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
                    if angle in canSee.keys():
                        canSee[angle].append((diffx ** 2 + diffy ** 2, (checkx, checky)))
                    else:
                        canSee[angle] = [(diffx ** 2 + diffy ** 2, (checkx, checky))]
    asteroidinfo = {}
    for angle in canSee.keys():
        asteroidinfo[angle] = [location[1] for location in sorted(canSee[angle])]
    return asteroidinfo


with open("Input/2019day10input.txt") as inputfile:
    grid = [list(line.strip()) for line in inputfile.readlines()]

numasteroids = {}
for y, row in enumerate(grid):
    for x, position in enumerate(row):
        if position == "#":  # if the square is an asteroid
            numasteroids[(x, y)] = findasteroids(x, y)

totalasteroids = len([ast for row in grid for ast in row if ast == "#"])
best = max(zip([len(canSee.keys()) for canSee in numasteroids.values()], numasteroids.keys()))[1]
asteroidinfo = numasteroids[best]
lasertargetangles = sorted(asteroidinfo.keys())

currasteroids = dict(zip(asteroidinfo.keys(), [v.copy() for v in asteroidinfo.values()]))  # copy the asteroidinfo
destroyed = []
while len(destroyed) < (totalasteroids - 1):
    for angle in lasertargetangles:
        try:
            destroyed.append(currasteroids[angle].pop(0))
        except IndexError:
            pass

print(correct := destroyed[199])
print(correct[0] * 100 + correct[1])
