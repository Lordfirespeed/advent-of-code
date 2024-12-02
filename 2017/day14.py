from day10 import knothash

inputhash = "hfdlxzhv"

array = []
totalfilled = 0
for line in range(128):
    hexhash = knothash(256, (inputhash + "-" + str(line)))
    binhash = ""
    for index in range(len(hexhash)):
        binchar = bin(int(hexhash[index], 16))[2:]
        while len(binchar) < 4:
            binchar = "0" + binchar
        binhash = binhash + binchar
    totalfilled += binhash.count("1")
    array.append(list(str(i) for i in binhash))
    #print(totalfilled)

output = False
if output:
    open("arrayhistory.txt", "w").close()
    with open("arrayhistory.txt", "a") as outputfile:
        for line in array:
            outputfile.write("".join(line) + "\n")
        outputfile.write("\n0\n\n")
                    
regions = 0
for lineindex, line in enumerate(array, 0):
    for charindex, char in enumerate(line, 0):
        if char == "1":
            onecoords = [[lineindex, charindex]]
            for oneloc in onecoords:
                try:
                    checkloc = [(oneloc[0] + 1), oneloc[1]]
                    if array[checkloc[0]][checkloc[1]] == "1" and not checkloc in onecoords:
                        onecoords.append(checkloc)
                except IndexError:
                    indexerror = 1
                    
                try:
                    checkloc = [(oneloc[0] - 1), oneloc[1]]
                    if array[checkloc[0]][checkloc[1]] == "1" and not checkloc in onecoords and not checkloc[0] == -1:
                        onecoords.append(checkloc)
                except IndexError:
                    indexerror = 1
                    
                try:
                    checkloc = [oneloc[0], (oneloc[1] + 1)]
                    if array[checkloc[0]][checkloc[1]] == "1" and not checkloc in onecoords:
                        onecoords.append(checkloc)
                except IndexError:
                    indexerror = 1

                try:
                    checkloc = [oneloc[0], (oneloc[1] - 1)]
                    if array[checkloc[0]][checkloc[1]] == "1" and not checkloc in onecoords and not checkloc[1] == -1:
                        onecoords.append(checkloc)
                except IndexError:
                    indexerror = 1
            
            for location in onecoords:
                array[location[0]][location[1]] = "X"
            regions += 1

            if output:
                with open("arrayhistory.txt", "a") as outputfile:
                    for line in array:
                        outputfile.write("".join(line) + "\n")
                    outputfile.write("\n" + str(regions) + "\n\n")

print(regions)
