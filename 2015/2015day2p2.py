with open("day2input.txt") as inputfile:
    inputlist = [line.strip() for line in inputfile.readlines()]
inputlist = [list(map(int, cuboid.split("x"))) for cuboid in inputlist]

total = 0
for cuboid in inputlist:
    sidea = cuboid[0]
    sideb = cuboid[1]
    sidec = cuboid[2]

    perima = (2 * sidea) + (2 * sideb)
    perimb = (2 * sidea) + (2 * sidec)
    perimc = (2 * sideb) + (2 * sidec)
    volume = sidea * sideb * sidec

    total += min([perima, perimb, perimc]) + volume

print(total)