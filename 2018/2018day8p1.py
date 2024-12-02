with open("2018day8input.txt") as inputfile:
    inputlist = [int(number) for line in inputfile.readlines() for number in line.strip().split(" ")]


def getnode(index):
    metadata = []
    nochildren = inputlist[index]
    nometadata = inputlist[index+1]
    nextindex = index + 2
    if nochildren > 0:
        for childno in range(0, nochildren):
            node = getnode(nextindex)
            nextindex = node[0]
            metadata += node[1]
    if nometadata > 0:
        for metano in range(0, nometadata):
            metadata.append(inputlist[nextindex])
            nextindex += 1
    return [nextindex, metadata]


print(sum(getnode(0)[1]))
