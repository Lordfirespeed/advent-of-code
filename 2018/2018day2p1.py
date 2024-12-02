from string import ascii_lowercase as alphabet


def countletters(string):
    letterdict = {}
    for letter in alphabet:
        letterdict[letter] = string.count(letter)
    letterdict = dict([[letter, letterdict[letter]] for letter in letterdict if letterdict[letter] != 0])
    return dict(letterdict)


with open("2018day2input.txt") as inputfile:
    inputlines = [line.strip() for line in inputfile.readlines()]

doubleletters = 0
tripleletters = 0
for key in inputlines:
    countedletters = countletters(key)
    values = [countedletters[letter] for letter in countedletters]
    doubleletter = any([value == 2 for value in values])
    tripleletter = any([value == 3 for value in values])
    doubleletters += int(doubleletter)
    tripleletters += int(tripleletter)

checksum = doubleletters * tripleletters
print("Checksum: " + str(checksum))
