with open("Input/2019day5input.txt") as inputfile:
    nums = [int(n) for n in inputfile.readline().strip().split(",")]

paramlengths = {1: 4, 2: 4, 3: 2, 4: 2, 99: 1}


def inp():
    return 1


def out(x):
    print(x)


def parse(command, register):
    operator = str(command[0])
    opcode = int(operator[-2:])
    paramlength = paramlengths[opcode]
    modes = [int(("0"*paramlength + operator[:-2])[-i]) for i in range(1, paramlength)]
    # print(modes)
    if opcode == 1:
        register[command[3]] = (command[1] if modes[0] else register[command[1]]) + (command[2] if modes[1] else register[command[2]])
    elif opcode == 2:
        register[command[3]] = (command[1] if modes[0] else register[command[1]]) * (command[2] if modes[1] else register[command[2]])
    elif opcode == 3:
        register[command[1]] = inp()
    elif opcode == 4:
        out(command[1] if modes[0] else register[command[1]])


currindex = 0
done = False
while not done:
    if (opcode := int(str(nums[currindex])[-2:])) not in paramlengths.keys():
        print(f"Failed: opcode {nums[currindex]} at index {currindex} not found.")
        done = True
    else:
        if opcode == 99:
            done = True
        else:
            paramlength = paramlengths[opcode]
            command = nums[currindex:currindex+paramlength]
            # print(command)
            parse(command, nums)
            currindex += paramlength
