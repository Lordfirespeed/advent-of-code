with open("2016day9input.txt") as inputfile:
    inputstring = "".join([line.strip() for line in inputfile.readlines()]).replace(" ", "")

outstring = ""
index = 0
while index < len(inputstring):
    if inputstring[index] == "(":
        startmarker = index
        endmarker = inputstring.index(")", index)
        strlength, repeat = list(map(int, inputstring[startmarker+1:endmarker].split("x")))
        jumpto = endmarker+strlength+1
        outstring += (inputstring[endmarker+1:endmarker+strlength+1] * repeat)
        index = jumpto
    else:
        outstring += inputstring[index]
        index += 1

print(len(outstring))
