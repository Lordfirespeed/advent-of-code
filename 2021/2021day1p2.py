with open(r"Input\2021day1.txt") as inputFile:
    inputNums = [int(line.strip()) for line in inputFile.readlines()]

trios = zip(inputNums[:-2], inputNums[1:-1], inputNums[2:])
sums = [third + second + first for first, second, third in trios]

pairs = zip(sums[:-1], sums[1:])
answer = [second > first for first, second in pairs].count(True)

print(f"The answer is {answer}")
