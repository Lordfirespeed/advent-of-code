def findmostcommon(string):
    instances = []
    for character in "abcdefghijklmnopqrstuvwxyz":
        instances.append([string.count(character), character])
    return [instance for instance in instances if instance[0] > 0]

with open("2016day4input.txt") as inputfile:
    inputlist = [line.strip() for line in inputfile.readlines()]

totalID = 0
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
    if formchecknum == checknum:
        totalID += ID
print(totalID)
