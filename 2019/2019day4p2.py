from itertools import product


def group(array):
    groups = []
    for var in array:
        try:
            if var == groups[-1][-1]:
                groups[-1].append(var)
            else:
                groups.append([var])
        except IndexError:
            groups.append([var])
    return groups


inp = range(271973, 785961)
total = 0

for nums in product(range(10), repeat=6):
    if (num := int("".join([str(n) for n in nums]))) in inp:
        groups = group(nums)
        pairfound = [len(adj) for adj in groups].count(2) > 0
        if tuple(sorted(nums)) == nums and pairfound:
            total += 1

print(f"Total: {total}")
