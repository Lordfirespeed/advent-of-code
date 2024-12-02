with open("Input/2019day1input.txt") as inputfile:
    nums = [int(line.strip()) for line in inputfile.readlines()]


def getfuel(mass):
    v = mass // 3 - 2
    return v + getfuel(v) if v > 0 else 0


req = [getfuel(n) for n in nums]
print(sum(req))
