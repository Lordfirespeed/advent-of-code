with open("2016day3input.txt") as inputfile:
    inputlist = [line.strip().split("  ") for line in inputfile.readlines()]
inputlist = [[int(length) for length in triangle if length != ''] for triangle in inputlist]

valid = []
for triangle in inputlist:
    a = int(triangle[0])
    b = int(triangle[1])
    c = int(triangle[2])
    if ((a + b) > c and (a + c) > b and (b + c) > a):
        valid.append(list(triangle))
    
print(len(inputlist))
print(len(valid))
