import re
from string import ascii_lowercase as alphabet

with open("2018day7input.txt") as inputfile:
    inputlist = [line.strip().lower() for line in inputfile]

findstep = re.compile("step [a-z]")
inputdata = [[match[-1] for match in findstep.findall(line)] for line in inputlist]

steps = dict([[letter, []] for letter in alphabet])
allstepids = []
for instruction in inputdata:
    steps[instruction[1]].append(instruction[0])
    allstepids += instruction

allstepids = list(set(allstepids))
allstepids.sort()
execsteps = dict(steps)
complete = []
executeorder = ""

while not complete == allstepids:
    possible = [stepid for stepid in execsteps if all([checkstepid in complete for checkstepid in execsteps[stepid]])]
    possible.sort()
    complete.append(possible[0])
    del execsteps[possible[0]]
    executeorder += possible[0]
    complete.sort()

print(executeorder.upper())
