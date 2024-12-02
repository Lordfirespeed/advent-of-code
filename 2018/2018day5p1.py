from string import ascii_lowercase
from string import ascii_uppercase

with open("2018day5input.txt") as inputfile:
    inputlines = [line.strip() for line in inputfile.readlines()]

inputstring = "".join(inputlines)
mappartA, mappartB = ascii_lowercase + ascii_uppercase, ascii_uppercase + ascii_lowercase
mapdict = dict([[mappartA[letterindex], mappartB[letterindex]] for letterindex in range(len(mappartA))])

runnoedit = False
while not runnoedit:
    runnoedit = True
    for index in range(0, len(inputstring)-1):
        if inputstring[index] == mapdict[inputstring[index+1]]:
            inputstring = inputstring[:index] + inputstring[index+2:]
            runnoedit = False
            break

print("Result: " + str(len(inputstring)))
