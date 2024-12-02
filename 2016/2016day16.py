def extend(binstring, disklen):
    returnstring = binstring
    while len(returnstring) < disklen:
        a = returnstring
        b = returnstring[::-1].replace("0", "X").replace("1", "0").replace("X", "1")
        returnstring = a + "0" + b
    return returnstring[:disklen]

def checksum(binstring):
    length = len(binstring)
    value = ""
    for index in range(0, length, 2):
        value += str(int(binstring[index] == binstring[index+1]))
    if len(value) % 2 == 0:
        value = checksum(value)
    return value

inputstring = "10111011111001111"
disklen = 272
seconddisk = 35651584
print(checksum(extend(inputstring, disklen)))
print(checksum(extend(inputstring, seconddisk)))
