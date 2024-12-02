paramlengths = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2, 99: 1}


class IntcodeComputer(object):
    def __init__(self, name, register, inps=()):
        global paramlengths
        self.initregister = register.copy()
        self.register = register.copy()
        self.inps = (list(inps) if type(inps) == tuple else inps.copy()) if type(inps) == tuple or type(inps) == list else [inps]
        self.initinps = self.inps.copy()
        self.inputindex = 0
        self.outs = []
        self.currindex = 0
        self.name = name
        self.done = False
        self.relativebase = 0

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def reset(self):
        self.register = self.initregister.copy()
        self.inputindex = 0
        self.inps = self.initinps.copy()
        self.currindex = 0
        self.outs = []
        self.done = False
        self.relativebase = 0

    def select(self, command, modes, index):
        if modes[index - 1] == 0:
            try:
                return self.register[command[index]]
            except IndexError:
                self.register += [0 for _ in range(command[index] - len(self.register))]
                return 0
        if modes[index - 1] == 1:
            return command[index]
        if modes[index - 1] == 2:
            try:
                return self.register[command[index] + self.relativebase]
            except IndexError:
                self.register += [0 for _ in range(command[index] + self.relativebase - len(self.register))]

    def addinp(self, val):
        self.inps.append(val)

    def out(self, val):
        self.outs.append(val)

    def parse(self, command):
        try:
            operator = str(command[0])
            opcode = int(operator[-2:])
            paramlength = paramlengths[opcode]
            modes = [int(("0" * paramlength + operator[:-2])[-i]) for i in range(1, paramlength)]
            # print(modes)
            newindex = self.currindex
            if opcode == 1:
                # print(self.select(command, modes, 1))
                # print(self.select(command, modes, 2), command, modes)
                # print(self.relativebase, command[3])

                self.register[command[3] if modes[2] == 0 else (self.relativebase + command[3])] = self.select(command, modes, 1) + self.select(command, modes, 2)
            elif opcode == 2:
                self.register[command[3] if modes[2] == 0 else (self.relativebase + command[3])] = self.select(command, modes, 1) * self.select(command, modes, 2)
            elif opcode == 3:
                try:
                    # print(modes)
                    # print(self.inps)
                    self.register[command[1] if modes[0] == 0 else (self.relativebase + command[1])] = (taken := self.inps[self.inputindex])
                    # print("TAKEN", taken)
                    self.inputindex += 1
                    newindex = self.currindex + paramlength
                except IndexError:
                    newindex = self.currindex
                    self.done = True
            elif opcode == 4:
                self.out(self.select(command, modes, 1))
            elif opcode == 5:
                val = self.select(command, modes, 1)
                # print(val)
                if val:
                    newindex = self.select(command, modes, 2)
                    # print(newindex)
                else:
                    newindex = self.currindex + paramlength
            elif opcode == 6:
                val = self.select(command, modes, 1)
                if not val:
                    newindex = self.select(command, modes, 2)
                else:
                    newindex = self.currindex + paramlength
            elif opcode == 7:
                self.register[command[3] if modes[2] == 0 else (self.relativebase + command[3])] = int(self.select(command, modes, 1) < self.select(command, modes, 2))
            elif opcode == 8:
                self.register[command[3] if modes[2] == 0 else (self.relativebase + command[3])] = int(self.select(command, modes, 1) == self.select(command, modes, 2))
            elif opcode == 9:
                self.relativebase += self.select(command, modes, 1)

            return self.currindex + paramlength if opcode not in (3, 5, 6) else newindex
        except IndexError:
            self.register += [0, 0, 0]
            return self.parse(command)

    def execute(self):
        self.done = False
        opcode = 0
        while not self.done:
            if (opcode := int(str(self.register[self.currindex])[-2:])) not in paramlengths.keys():
                print(f"Failed: opcode {self.register[self.currindex]} at index {self.currindex} not found.")
                self.done = True
            else:
                if opcode == 99:
                    self.done = True
                else:
                    paramlength = paramlengths[opcode]
                    command = self.register[self.currindex:self.currindex + paramlength]
                    self.currindex = self.parse(command)
                    # print(self.register, self.currindex, command)
        # print(self.outs)
        return self.outs, opcode == 99


def printgrid(grid):
    totalpainted = 0
    xvals, yvals = zip(*grid.keys())
    minx, maxx, miny, maxy = min(xvals), max(xvals), min(yvals), max(yvals)
    for y in range(maxy, miny - 1, -1):
        line = ""
        for x in range(minx, maxx + 1):
            if not (x, y) in grid.keys():
                line = line + " "
            else:
                line = line + grid[(x, y)]
        totalpainted += line.count("#")
        print(line)
    return totalpainted


with open("Input/2019day11input.txt") as inputfile:
    startregister = [int(n) for n in inputfile.readline().strip().split(",")]

facingdict = {0: (0, 1), 90: (1, 0), 180: (0, -1), 270: (-1, 0)}
turndict = {0: -90, 1: 90}
painteddict = {" ": 0, "#": 1}

robotcomp = IntcodeComputer("robot", startregister, 0)
robotfacing = 0
robotlocation = {"x": 0, "y": 0}
painted = {(0, 0): "#"}
done = False
while not done:
    vals, done = robotcomp.execute()
    if vals[-2]:
        painted[(robotlocation["x"], robotlocation["y"])] = "#"
    else:
        painted[(robotlocation["x"], robotlocation["y"])] = " "
    robotfacing = (robotfacing + turndict[vals[-1]]) % 360
    move = facingdict[robotfacing]
    robotlocation["x"] += move[0]
    robotlocation["y"] += move[1]
    try:
        robotcomp.addinp(painteddict[painted[(robotlocation["x"], robotlocation["y"])]])
    except KeyError:
        robotcomp.addinp(0)
    #print(robotlocation, robotfacing)

print(len(painted.keys()))
