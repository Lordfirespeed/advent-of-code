from itertools import combinations
from math import prod as product

with open(r"Input\2020day1.txt") as inputfile:
    inputlist = [int(line.strip()) for line in inputfile.readlines()]

solution = None

for combinations in combinations(inputlist, 3):
    if sum(combinations) == 2020:
        solution = combinations
        break

print(f"Solution found: {solution}. Product: {product(solution)}")
