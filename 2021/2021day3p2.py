with open(r"Input\2021day3.txt") as inputFile:
    inputLines = [line.strip() for line in inputFile.readlines()]

oxygenNums = inputLines.copy()
co2Nums = inputLines.copy()

oxygenBitPosition = 0
while len(oxygenNums) > 1:
    column = [num[oxygenBitPosition] for num in oxygenNums]
    mostCommon = "1" if column.count("1") >= len(column)/2 else "0"
    oxygenNums = [num for num in oxygenNums if num[oxygenBitPosition] == mostCommon]
    oxygenBitPosition += 1

co2BitPosition = 0
while len(co2Nums) > 1:
    column = [num[co2BitPosition] for num in co2Nums]
    leastCommon = "0" if column.count("1") >= len(column)/2 else "1"
    co2Nums = [num for num in co2Nums if num[co2BitPosition] == leastCommon]
    co2BitPosition += 1

oxygen = int("0b"+oxygenNums[0], 2)
co2 = int("0b"+co2Nums[0], 2)

answer = oxygen * co2

print(f"The answer is {answer}")
