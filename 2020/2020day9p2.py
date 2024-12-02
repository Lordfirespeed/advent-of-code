from itertools import combinations

with open(r"Input\2020day9.txt") as inputfile:
    inputnums = [int(line.strip()) for line in inputfile.readlines()]

target = 21806024

range_len = len(inputnums)
found = False
while not found:
    ranges = [inputnums[starti:range_len+starti] for starti in range(len(inputnums)-range_len)]
    for check in ranges:
        if sum(check) == target:
            found = check
            break
    range_len -= 1

print(f"Sum of smallest and largest in contiguous set: {min(found) + max(found)}")
