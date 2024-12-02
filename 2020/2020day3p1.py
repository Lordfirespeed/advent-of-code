with open(r"Input\2020day3.txt") as inputfile:
    inputlines = [line.strip() for line in inputfile.readlines()]

slope = (3, 1)
position = (0, 0)
path = []

while position[1] < len(inputlines):
    path.append(inputlines[position[1]][position[0] % len(inputlines[position[1]])])
    position = (position[0] + slope[0], position[1] + slope[1])

print(f"Path: {''.join(path)}")
print(f"Number of trees: {path.count('#')}")
