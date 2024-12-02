with open("2018day1input.txt") as inputfile:
    inputlines = [line.strip() for line in inputfile.readlines()]

frequency = 0
visitedfreqs = [0]
found = False
while not found:
    for line in inputlines:
        frequency += int(line)
        if frequency in visitedfreqs:
            found = True
            break
        visitedfreqs.append(int(frequency))

print("Frequency: " + str(frequency))