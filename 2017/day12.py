with open("day12input.txt") as fileinput:
    inputdict = {}
    for line in fileinput.readlines():
        line = line.rstrip()
        citizen = int(line[:line.index(" ")])
        communicates = (line[(line.index("> ") + 2):]).split(", ")
        communicates = [int(thing) for thing in communicates]
        inputdict[citizen] = communicates

#inputdict = {0:[2], 1:[1], 2:[0, 3, 4], 3:[2, 4], 4:[2, 3, 6], 5:[6], 6:[4, 5]}

def partone():
    talkstozero = inputdict[0]
    for citizen in talkstozero:
        for contact in inputdict[citizen]:
            if not contact in talkstozero:
                talkstozero.append(contact)

    return len(talkstozero)

def parttwo():
    checkdict = inputdict
    checkedpeople = []
    groups = []
    groupindex = 0
    for citizen in checkdict:
        if not citizen in checkedpeople:
            talksto = inputdict[citizen]
            for othercitizen in talksto:
                for contact in inputdict[othercitizen]:
                    if not contact in talksto:
                        talksto.append(contact)
            groups.append(talksto)
            groupindex += 1
            for person in talksto:
                checkedpeople.append(person)
                
    return len(groups)
            
            
