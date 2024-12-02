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
workers = [["", 0]] * 5

time = 0
while not complete == allstepids:
    for worker in workers:
        if worker[1] == 0 and worker[0] != "":
            complete.append(worker[0])
    possible = [stepid for stepid in execsteps if all([checkstepid in complete for checkstepid in execsteps[stepid]])]
    possible.sort()
    for index, worker in enumerate(workers):
        if worker[1] == 0:
            if any(possible):
                worker = [possible[0], 61 + alphabet.index(possible[0])]
                del execsteps[possible[0]]
                del possible[0]
            else:
                worker = ["", 0]
            workers[index] = list(worker)
    time += 1
    workers = [[worker[0], worker[1]-1] if worker[1] != 0 else worker for worker in workers]
    complete.sort()

print(str(time-1))
