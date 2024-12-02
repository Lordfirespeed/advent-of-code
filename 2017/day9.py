def checkcancel(string, index):
    discovered = False
    checkindex = index - 1
    valid = True
    while discovered is False:
        if (string[checkindex] == "!"):
            if valid:
                valid = False
            else:
                valid = True
            checkindex -= 1
        else:
            break
    return valid

def cleanup():
    with open("day9input.txt") as inputfile:
        inputstuff = inputfile.readlines()[0].rstrip()
    garbage = False
    outputlist = []
    index = 0
    removedamount = 0
    removed = []
    while index <= (len(inputstuff) - 1):
        character = inputstuff[index]

        if garbage and not character == ">":
            if character != "!" and (checkcancel(inputstuff, index)):
                removedamount += 1
                removed.append(character)
            else:
                removed.append("*")
        else:
            removed.append("*")
        
        if character == "!":
            index += 1
        elif character == "<" and not garbage:
            garbage = True

            
        if not garbage:
                outputlist.append(character)
        if character == ">" and garbage:
            if inputstuff[index+1] == ",":
                index += 1
            garbage = False
        
            
        index += 1

    print(str(removedamount) + " characters of garbage removed.")
    return ("".join(outputlist))


def score():
    cleaninput = cleanup()
    totalscore = 0
    depth = 1
    index = 0
    while index <= (len(cleaninput) - 1):
        character = cleaninput[index]
        if character == "{":
            totalscore += depth
            depth += 1
        elif character == "}":
            depth -= 1
        index += 1
    return totalscore
            
        


    

    
