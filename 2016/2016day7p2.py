def checkaba(string):
    return (string[0] == string[2]) and (string[0] != string[1])

def splitsections(string):
    outside = []
    inside = []
    leftbracketindex = string.index("[")
    rightbracketindex = string.index("]")
    outside.append(string[:leftbracketindex])
    outside.append(string[rightbracketindex+1:])
    inside.append(string[leftbracketindex+1:rightbracketindex])
    
    if "[" in outside[-1]:
        checkright = splitsections(outside[-1])
        del outside[-1]
        outside += (checkright["outside"])
        inside += (checkright["inside"])
            
    return {"outside":list(outside), "inside":list(inside)}
    
with open("2016day7input.txt") as inputfile:
    inputlist = [line.strip() for line in inputfile.readlines()]

valid = []
for line in inputlist:
    lookingfor = []
    sections = splitsections(line)

    for string in sections["inside"]:
        for index in range(len(string)-2):
            if checkaba(string[index:index+3]):
                lookingfor.append(string[index+1] + string[index] + string[index+1])

    validbool = False
    for string in sections["outside"]:
        for findstring in lookingfor:
            if findstring in string:
                validbool = True

    if validbool:
        valid.append(line)
        
print(len(valid))
