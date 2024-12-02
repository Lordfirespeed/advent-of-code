from string import ascii_lowercase
from string import ascii_uppercase


def getlength(string):
    runnoedit = False
    while not runnoedit:
        runnoedit = True
        index = 0
        while index < len(string) - 1:
            if string[index] == mapdict[string[index + 1]]:
                string = string[:index] + string[index + 2:]
                index -= 2
                runnoedit = False
            index += 1
    return len(string)


with open("2018day5input.txt") as inputfile:
    inputlines = [line.strip() for line in inputfile.readlines()]

inputstring = "".join(inputlines)
mappartA, mappartB = ascii_lowercase + ascii_uppercase, ascii_uppercase + ascii_lowercase
mapdict = dict([[mappartA[letterindex], mappartB[letterindex]] for letterindex in range(len(mappartA))])

lengths = []
for character in ascii_lowercase:
    usestring = inputstring.replace(character, "")
    usestring = usestring.replace(character.upper(), "")
    lengths.append(getlength(usestring))
    print("Got length for character '" + character.upper() + "' successfully.")

print("Result: " + str(min(lengths)))
