from sys import exit


def comparestrings(stringa, stringb):
    samechars = []
    for index in range(len(stringa)):
        samechars.append(stringa[index] == stringb[index])
    return samechars


def generatestrings(string):
    possiblestrings = [string[:index] + string[index+1:] for index in range(len(string))]
    return possiblestrings


with open("2018day2input.txt") as inputfile:
    inputlines = [line.strip() for line in inputfile.readlines()]

found = False
for keyindex, key in enumerate(inputlines):
    # For every key in the list
    for checkkey in (inputlines[:keyindex] + inputlines[keyindex+1:]):
        # Check it against every checkkey in the list except for itself
        keypossible = generatestrings(key)
        checkkeypossible = generatestrings(checkkey)
        checkequal = [keypossible[index] == checkkeypossible[index] for index in range(len(keypossible))]
        if any(checkequal):
            print("Common Letters: " + keypossible[checkequal.index(True)])
            exit()
