with open("2016day9input.txt") as inputfile:
    inputstring = "".join([line.strip() for line in inputfile.readlines()]).replace(" ", "")

def decode(string):
    if not "(" in string:
        return string
    index = 0
    outstring = ""
    while index < len(string):
        if string[index] == "(":
            startmarker = index
            endmarker = string.index(")", index+1)
            strlength, repeat = list(map(int, string[startmarker+1:endmarker].split("x")))
            jumpto = endmarker+strlength+1
            outstring += decode(string[endmarker+1:endmarker+strlength+1]) * repeat
            index = jumpto
        else:
            outstring += inputstring[index]
            index += 1
    return outstring
            
finalstring = decode(inputstring)
print(len(finalstring))
