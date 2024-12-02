from itertools import permutations

paramlengths = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 99: 1}


class IntcodeComputer(object):
    def __init__(self, name, register, inps=()):
        global paramlengths
        self.register = register.copy()
        self.inps = (tuple(inps.copy()) if type(inps) == list else inps) if type(inps) == tuple or type(inps) == list else tuple([inps])
        self.input = self.gen()
        self.outs = []
        self.currindex = 0
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def gen(self):
        for val in self.inps:
            yield val

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
            self.register[command[1]] = (taken := next(self.input))
            # print("TAKEN", taken)
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

        return self.currindex + paramlength if opcode not in (5, 6) else newindex

    def execute(self):
        done = False
        while not done:
            if (opcode := int(str(self.register[self.currindex])[-2:])) not in paramlengths.keys():
                print(f"Failed: opcode {self.register[self.currindex]} at index {self.currindex} not found.")
                done = True
            else:
                if opcode == 99:
                    done = True
                else:
                    paramlength = paramlengths[opcode]
                    command = self.register[self.currindex:self.currindex + paramlength]
                    self.currindex = self.parse(command)
                    # print(self.register)
        return self.outs


with open("Input/2019day7input.txt") as inputfile:
    startregister = [int(n) for n in inputfile.readline().strip().split(",")]

thrusts = []
for phasesettings in permutations(range(5)):
    thrust = 0
    # print(phasesettings)
    for phase, ampname in zip(phasesettings, ["A", "B", "C", "D", "E"]):
        amp = IntcodeComputer("Amp" + ampname, startregister, (phase, thrust))
        thrust = amp.execute()[0]
        # print(thrust)
    thrusts.append((thrust, phasesettings))

print(max(thrusts))
