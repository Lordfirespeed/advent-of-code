import re


def gettimestamp(string):
    # Returns a list containing [Year, Month, Day, Minute, Hour] from a timestamped input line
    matches = findtimestamp.finditer(string)
    for match in matches:
        values = findintegers.findall(string[match.span()[0]:match.span()[1]])
        return values
    return None


findtimestamp = re.compile(r"\[[\w\- :]*\]")
findintegers = re.compile(r"\d+")

with open("2018day4input.txt") as inputfile:
    inputlines = [line.strip() for line in inputfile.readlines()]

inputdata = [[gettimestamp(line), line[line.index("]")+2:]] for line in inputlines]
inputdata = [[int("".join(data[0]))] + data for data in inputdata]
inputdata.sort()

minutes = {}
guard = 0
fellasleep = 0
wokeup = 0
for command in inputdata:
    integers = findintegers.findall(command[2])
    if integers:
        guard = int(integers[0])
    elif command[2] == "falls asleep":
        fellasleep = int("".join(command[1][-2:]))
    elif command[2] == "wakes up":
        wokeup = int("".join(command[1][-2:]))
        for minute in range(fellasleep, wokeup):
            if minute not in minutes:
                minutes[minute] = {}
            if guard not in minutes[minute]:
                minutes[minute][guard] = 0
            minutes[minute][guard] += 1

maxguard = 0
maxminute = 0
maxcount = 0
for minute in minutes:
    for guard in minutes[minute]:
        if minutes[minute][guard] > maxcount:
            maxcount = minutes[minute][guard]
            maxguard = guard
            maxminute = minute

print("Result: " + str(maxminute * maxguard))
