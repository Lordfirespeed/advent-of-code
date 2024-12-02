inputlist = []
playedsounds = []
recovered = []
with open("day18input.txt") as inputfile:
    for line in inputfile.readlines():
        line = line.rstrip()
        inputlist.append(line.split(" "))
# set up core lists and retrieve input from file

from string import ascii_lowercase
values = ("0" + (25 * ",0")).split(",")
values = [int(value) for value in values]
# to map an alphabetic register name to the value list:
# values[ascii_lowercase.index(register)]

currentinstruction = 0

def snd(register):
    # play sound (append to list) of frequency equal to value of register
    playedsounds.append(values[ascii_lowercase.index(register)])

def set(register, value):
    # set register to value
    try:
        values[ascii_lowercase.index(register)] = int(value)
    except ValueError:
        values[ascii_lowercase.index(register)] = values[ascii_lowercase.index(value)]

def add(register, adder):
    # add adder to register value
    try:
        values[ascii_lowercase.index(register)] += int(adder)
    except ValueError:
        values[ascii_lowercase.index(register)] += values[ascii_lowercase.index(adder)]

def mul(register, factor):
    # multiply register value by factor]
    try:
        values[ascii_lowercase.index(register)] *= int(factor)
    except ValueError:
        values[ascii_lowercase.index(register)] *= values[ascii_lowercase.index(factor)]

def mod(register, divisor):
    # set register to its value modulo the divisor
    try:
        values[ascii_lowercase.index(register)] %= int(divisor)
    except ValueError:
        values[ascii_lowercase.index(register)] %= values[ascii_lowercase.index(divisor)]

def rcv(register):
    # recover last sound frequency, if register value is not zero
    if values[ascii_lowercase.index(register)] != 0:
        recovered.append(playedsounds[-1])

def jgz(register, value):
    # jumps instructions by value if register's value is greater than zero
    global currentinstruction
    if values[ascii_lowercase.index(register)] > 0:
        currentinstruction += int(value)

while currentinstruction < len(inputlist):
    commandlist = inputlist[currentinstruction]
    if len(commandlist) == 3:
        command = (commandlist[0] + "('" + commandlist[1] + "', '" + commandlist[2] + "')")
        print(command)
        exec(command)
    else:
        command = (commandlist[0] + "('" + commandlist[1] + "')")
        print(command)
        exec(command)
    currentinstruction += 1
    if recovered:
        break
print(recovered)



    
