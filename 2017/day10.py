def knothash(totallength, inputstring):
    numbers = list(range(totallength))
    #inputstring = "189,1,111,246,254,2,0,120,215,93,255,50,84,15,94,62"
    inputlist = [ord(c) for c in inputstring]
    inputlist += [17, 31, 73, 47, 23]
    skip = 0
    currentposition = 0

    for rounds in range(64):
        for index, length in enumerate(inputlist, 1):
            circlenums = numbers + numbers
            if currentposition >= totallength:
                currentposition = currentposition % totallength
            #print(currentposition)
            selected = circlenums[(currentposition):(currentposition + length)]
            flipped = list(reversed(selected))
            insertindex = currentposition
            for number in flipped:
                if insertindex >= totallength:
                    insertindex -= totallength
                numbers[insertindex] = number
                insertindex += 1
            
            currentposition += length + skip
            skip += 1

    groupedlist = []
    for x in range(int(totallength/16)):
        groupedlist.append(numbers[(16 * x):(16 * (x + 1))])

    densehashlist = []
    for group in groupedlist:
        xornum = 0
        for number in group:
            xornum ^= number
        densehashlist.append(xornum)

    hexlist = []
    for item in densehashlist:
        if len(str(hex(item))[2:]) < 2:
            hexed = '0' + str(hex(item))[2:]
        else:
            hexed = str(hex(item))[2:]
        hexlist.append(hexed)

    return ("".join(hexlist))
