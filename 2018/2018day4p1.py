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

guards = {}
guard = 0
fellasleep = 0
wokeup = 0
for command in inputdata:
    integers = findintegers.findall(command[2])
    if integers:
        guard = int(integers[0])
    elif command[2] == "falls asleep":
        fellasleep = command[0]
    elif command[2] == "wakes up":
        wokeup = command[0]
        timeasleep = wokeup - fellasleep
        if guard not in guards:
            guards[guard] = 0
        guards[guard] += timeasleep

timesasleep = dict([[guards[guard], guard] for guard in guards])
mostasleepguard = timesasleep[max(timesasleep)]

asleepminutes = {}
fellasleep = 0
wokeup = 0
guardactive = False
for command in inputdata:
    if command[2] == ("Guard #" + str(mostasleepguard) + " begins shift"):
        guardactive = True
    elif findintegers.match(command[2]):
        guardactive = False
    elif guardactive and command[2] == "falls asleep":
        fellasleep = int("".join(command[1][-3:]))
    elif guardactive and command[2] == "wakes up":
        wokeup = int("".join(command[1][-3:]))
        for minuteasleep in range(fellasleep, wokeup):
            if minuteasleep not in asleepminutes:
                asleepminutes[minuteasleep] = 0
            asleepminutes[minuteasleep] += 1

sleptminutes = dict([[asleepminutes[minute], minute] for minute in asleepminutes])
mostasleepminute = int(str(sleptminutes[max(sleptminutes)])[-2:])
print("Result: " + str(mostasleepguard * mostasleepminute))
