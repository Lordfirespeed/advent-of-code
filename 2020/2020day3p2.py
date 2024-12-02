from math import prod as product

with open(r"Input\2020day3.txt") as inputfile:
    inputlines = [line.strip() for line in inputfile.readlines()]


def get_path(slope):
    position = (0, 0)
    path = []

    while position[1] < len(inputlines):
        path.append(inputlines[position[1]][position[0] % len(inputlines[position[1]])])
        position = (position[0] + slope[0], position[1] + slope[1])

    return "".join(path)


slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

paths = [get_path(slope) for slope in slopes]
collisions = [path.count("#") for path in paths]

print(f"Product of collisions on all slopes: {product(collisions)}")
