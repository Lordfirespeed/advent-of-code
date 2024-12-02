with open(r"Input\2021day1.txt") as inputFile:
    inputNums = [int(line.strip()) for line in inputFile.readlines()]

pairs = zip(inputNums[:-1], inputNums[1:])
answer = [second > first for first, second in pairs].count(True)

print(f"The answer is {answer}")
