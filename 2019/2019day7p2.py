from itertools import permutations

paramlengths = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 99: 1}


class IntcodeComputer(object):
    def __init__(self, name, register, inps=()):
        global paramlengths
        self.register = register.copy()
        self.inps = (list(inps) if type(inps) == tuple else inps.copy()) if type(inps) == tuple or type(inps) == list else [inps]
        self.inputindex = 0
        self.outs = []
        self.currindex = 0
        self.name = name
        self.done = False

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def addinp(self, val):
        self.inps.append(val)

    def out(self, val):
        self.outs.append(val)

    def parse(self, command):
        operator = str(command[0])
        opcode = int(operator[-2:])
        paramlength = paramlengths[opcode]
        modes = [int(("0" * paramlength + operator[:-2])[-i]) for i in range(1, paramlength)]
        # print(modes)
        newindex = self.currindex
        if opcode == 1:
            self.register[command[3]] = (command[1] if modes[0] else self.register[command[1]]) + (
                command[2] if modes[1] else self.register[command[2]])
        elif opcode == 2:
            self.register[command[3]] = (command[1] if modes[0] else self.register[command[1]]) * (
                command[2] if modes[1] else self.register[command[2]])
        elif opcode == 3:
            try:
                self.register[command[1]] = (taken := self.inps[self.inputindex])
                # print("TAKEN", taken)
                self.inputindex += 1
                newindex = self.currindex + paramlength
            except IndexError:
                newindex = self.currindex
                self.done = True
        elif opcode == 4:
            self.out(command[1] if modes[0] else self.register[command[1]])
        elif opcode == 5:
            val = command[1] if modes[0] else self.register[command[1]]
            if val:
                newindex = command[2] if modes[1] else self.register[command[2]]
            else:
                newindex = self.currindex + paramlength
        elif opcode == 6:
            val = command[1] if modes[0] else self.register[command[1]]
            if not val:
                newindex = command[2] if modes[1] else self.register[command[2]]
            else:
                newindex = self.currindex + paramlength
        elif opcode == 7:
            self.register[command[3]] = int(
                (command[1] if modes[0] else self.register[command[1]]) < (command[2] if modes[1] else self.register[command[2]]))
        elif opcode == 8:
            self.register[command[3]] = int((command[1] if modes[0] else self.register[command[1]]) == (
                command[2] if modes[1] else self.register[command[2]]))

        return self.currindex + paramlength if opcode not in (3, 5, 6) else newindex

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
                    # print(self.register)
        # print(self.outs)
        return self.outs, opcode == 99


with open("Input/2019day7input.txt") as inputfile:
    startregister = [int(n) for n in inputfile.readline().strip().split(",")]

thrusts = []
for phasesettings in permutations(range(5, 10)):
    thrust = 0
    ampA = IntcodeComputer("AmpA", startregister, (phasesettings[0], thrust))
    thrust = int(ampA.execute()[0][-1])
    ampB = IntcodeComputer("AmpB", startregister, (phasesettings[1], thrust))
    thrust = int(ampB.execute()[0][-1])
    ampC = IntcodeComputer("AmpC", startregister, (phasesettings[2], thrust))
    thrust = int(ampC.execute()[0][-1])
    ampD = IntcodeComputer("AmpD", startregister, (phasesettings[3], thrust))
    thrust = int(ampD.execute()[0][-1])
    ampE = IntcodeComputer("AmpE", startregister, (phasesettings[4], thrust))
    thrust, done = ampE.execute()
    thrust = int(thrust[-1])
    while not done:
        ampA.addinp(thrust)
        thrust = int(ampA.execute()[0][-1])
        ampB.addinp(thrust)
        thrust = int(ampB.execute()[0][-1])
        ampC.addinp(thrust)
        thrust = int(ampC.execute()[0][-1])
        ampD.addinp(thrust)
        thrust = int(ampD.execute()[0][-1])
        ampE.addinp(thrust)
        thrust, done = ampE.execute()
        thrust = int(thrust[-1])
    thrusts.append((thrust, phasesettings))

print(max(thrusts))
