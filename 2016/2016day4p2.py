def findmostcommon(string):
    instances = []
    for character in "abcdefghijklmnopqrstuvwxyz":
        instances.append([string.count(character), character])
    return [instance for instance in instances if instance[0] > 0]

def shiftcypher(string, shift):
    charmap = ("abcdefghijklmnopqrstuvwxyz" * 2)
    returnstringlist = []
    for char in string:
        if char == "-":
            returnstringlist.append(" ")
        else:
            returnstringlist.append(charmap[charmap.index(char) + (shift % int(len(charmap) / 2))])
    return "".join(returnstringlist)

with open("2016day4input.txt") as inputfile:
    inputlist = [line.strip() for line in inputfile.readlines()]

with open("2016day4p2output.txt", "w") as outputfile:
    pass

for line in inputlist:
    checknum = line[line.index("[")+1:-1]
    chars = line[:line.index("[")]
    ID = chars[-3:]
    chars = chars.replace("-" + ID, "")
    ID = int(ID)
    # Pulls out string, ID, and checknum
    values = findmostcommon(chars)
    amounts = list(set([value[0] for value in values]))
    formchecknum = ""
    amountsindex = -1
    while len(formchecknum) < 5:
        formchecknum = formchecknum + "".join([value[1] for value in values if value[0] == amounts[amountsindex]])
        amountsindex -= 1
    formchecknum = formchecknum[:5]
    with open("2016day4p2output.txt", "a") as outputfile:
        decoded = shiftcypher(chars, ID)
        msg = decoded + ": " + str(ID) + "\n"
        outputfile.write(msg)
