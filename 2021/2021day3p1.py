with open(r"Input\2021day3.txt") as inputFile:
    inputLines = [line.strip() for line in inputFile.readlines()]

rotated = list(zip(*inputLines))
mostCommon = ""
for column in rotated:
    numOnes = column.count("1")
    if numOnes >= 500:
        mostCommon += "1"
    else:
        mostCommon += "0"

gamma = int(mostCommon, 2)
epsilon = int(mostCommon.replace("1", "Z").replace("0", "1").replace("Z", "0"), 2)

answer = gamma * epsilon

print(f"The answer is {answer}")
