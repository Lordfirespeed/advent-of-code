def findmostcommon(string):
    instances = []
    for character in "abcdefghijklmnopqrstuvwxyz":
        instances.append([string.count(character), character])
    return [instance for instance in instances if instance[0] > 0]

with open("2016day6input.txt") as inputfile:
    inputlisthorizontal = [line.strip() for line in inputfile.readlines()]

inputlistvertical = ["".join([line[index] for line in inputlisthorizontal]) for index in range(0, len(inputlisthorizontal[0]))]

day1 = ""
day2 = ""
for line in inputlistvertical:
    chars = findmostcommon(line)
    day1 = day1 + max(chars)[1]
    day2 = day2 + min(chars)[1]
    
print(day1, day2)
