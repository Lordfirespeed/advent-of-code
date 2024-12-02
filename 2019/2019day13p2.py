paramlengths = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2, 99: 1}
tiles = {0: " ", 1: "#", 2: "$", 3: "=", 4: "0"}
debug = False


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
        if type(val) == list or type(val) == tuple:
            self.inps += list(val)
        else:
            self.inps.append(val)

    def out(self, val):
        self.outs.append(val)

    def clrout(self):
        self.outs = []

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


def renderlisttodict(rendervals):
    return [rendervals[i:i+3] for i in range(0, len(rendervals), 3)]


def display(rendervals):
    global tiles
    renderpixels = renderlisttodict(rendervals)
    pixelsdict = {}
    segmentdisplay = False
    for pixel in renderpixels:
        x, y, tileid = pixel
        if (x, y) == (-1, 0):
            segmentdisplay = tileid
        else:
            pixelsdict[(x, y)] = tiles[tileid]
    xvals, yvals = zip(*pixelsdict.keys())
    for y in range(min(yvals), max(yvals)+1):
        line = ""
        for x in range(min(xvals), max(xvals)+1):
            try:
                line += pixelsdict[(x, y)]
            except KeyError:
                line += " "
        print(line) if debug else None
    return segmentdisplay


def find(rendervals):
    renderpixels = renderlisttodict(rendervals)[::-1]
    ball = renderpixels[[pixel[-1] for pixel in renderpixels].index(4)]
    paddle = renderpixels[[pixel[-1] for pixel in renderpixels].index(3)]
    return ball[:2], paddle[:2]


def decide(ballx, paddlex, balldirection):
    if balldirection:  # ball moving right
        if ballx == paddlex or ballx + 1 == paddlex:
            return 0
        elif ballx < paddlex:
            return -1
        elif ballx > paddlex:
            return 1
    else:
        if ballx == paddlex or ballx - 1 == paddlex:
            return 0
        elif ballx < paddlex:
            return -1
        elif ballx > paddlex:
            return 1


with open("Input/2019day13input.txt") as inputfile:
    startregister = [int(n) for n in inputfile.readline().strip().split(",")]

startregister[0] = 2
Arcade = IntcodeComputer("Arcade", startregister)

prevballlocation = None
currballdirection = None
currsegmentdisplay = 0
render, done = Arcade.execute()
newsegdisplay = display(render)
currsegmentdisplay = newsegdisplay if newsegdisplay else currsegmentdisplay
renderpixels = renderlisttodict(render)
minx, maxx = 1, len([loc for loc in renderpixels if loc[1] == 0]) - 1
currballlocation, currpaddlelocation = find(render)
Arcade.addinp(0)

while not done:
    prevballlocation = currballlocation.copy()
    render, done = Arcade.execute()
    newsegdisplay = display(render)
    currsegmentdisplay = newsegdisplay if newsegdisplay else currsegmentdisplay
    currballlocation, currpaddlelocation = find(render)
    currballdirection = currballlocation[0] > prevballlocation[0]
    if currballlocation[0] == minx or currballlocation[0] == maxx:
        currballdirection = not currballdirection
    move = decide(currballlocation[0], currpaddlelocation[0], currballdirection)
    print(move) if debug else None
    Arcade.addinp(move)

print(currsegmentdisplay)
