with open("2018day1input.txt") as inputfile:
    inputlines = [line.strip() for line in inputfile.readlines()]

frequency = 0
for line in inputlines:
    frequency += int(line)

print("Frequency: " + str(frequency))