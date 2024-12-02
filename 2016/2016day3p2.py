with open("2016day3input.txt") as inputfile:
    inputlist = [line.strip().split("  ") for line in inputfile.readlines()]
inputlistbad = [[int(length) for length in triangle if length != ''] for triangle in inputlist]

inputlist = []
for index in range(0, len(inputlistbad)-1, 3):
    line1 = inputlistbad[index]
    line2 = inputlistbad[index+1]
    line3 = inputlistbad[index+2]
    newline1 = [int(line1[0]), int(line2[0]), int(line3[0])]
    newline2 = [int(line1[1]), int(line2[1]), int(line3[1])]
    newline3 = [int(line1[2]), int(line2[2]), int(line3[2])]
    inputlist.append(newline1)
    inputlist.append(newline2)
    inputlist.append(newline3)

valid = []
for triangle in inputlist:
    a = int(triangle[0])
    b = int(triangle[1])
    c = int(triangle[2])
    if ((a + b) > c and (a + c) > b and (b + c) > a):
        valid.append(list(triangle))
    
print(len(inputlist))
print(len(valid))
