with open("Input/2019day1input.txt") as inputfile:
    nums = [int(line.strip()) for line in inputfile.readlines()]

req = [n // 3 - 2 for n in nums]
print(sum(req))
