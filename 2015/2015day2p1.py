with open("day2input.txt") as inputfile:
    inputlist = [line.strip() for line in inputfile.readlines()]
inputlist = [list(map(int, cuboid.split("x"))) for cuboid in inputlist]

total = 0
for cuboid in inputlist:
    sidea = cuboid[0]
    sideb = cuboid[1]
    sidec = cuboid[2]

    surfacea = sidea * sideb
    surfaceb = sidea * sidec
    surfacec = sideb * sidec

    total += (2 * surfacea) + (2 * surfaceb) + (2 * surfacec) + min([surfacea, surfaceb, surfacec])

print(total)