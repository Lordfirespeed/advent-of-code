with open("day5input.txt") as inputfile:
    inputlist = [line.strip() for line in inputfile.readlines()]


def checkdoublepairs(string):
    doubles = [string[index] + string[index+1] for index in range(len(string)-1)]
    for doubleindex, doublechar in enumerate(doubles):
        for checkindex, checkdouble in enumerate(doubles):
            if abs(doubleindex-checkindex) <= 1:
                pass
            elif doublechar == checkdouble:
                 return doublechar
    return False


def repeatgapchar(string):
    if len(string) < 3:
        return False
    for index, character in enumerate(string[:-2]):
        if character == string[index+2]:
            return character
    return False


good = []
for line in inputlist:
    if checkdoublepairs(line) and repeatgapchar(line):
        good.append(line)

print(len(good))
