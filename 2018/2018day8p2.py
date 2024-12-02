with open("2018day8input.txt") as inputfile:
    inputlist = [int(number) for line in inputfile.readlines() for number in line.strip().split(" ")]


def getvalue(index):
    value = 0
    valuechildren = []
    metadata = []
    nochildren = inputlist[index]
    nometadata = inputlist[index+1]
    nextindex = index + 2
    if nochildren > 0:
        for childno in range(0, nochildren):
            node = getvalue(nextindex)
            nextindex = node[0]
            valuechildren.append(node[1])
    if nometadata > 0:
        for metano in range(0, nometadata):
            try:
                value += valuechildren[inputlist[nextindex] - 1]
            except IndexError:
                pass
            metadata.append(inputlist[nextindex])
            nextindex += 1
    return [nextindex, value] if nochildren > 0 else [nextindex, sum(metadata)]


print(getvalue(0)[1])
