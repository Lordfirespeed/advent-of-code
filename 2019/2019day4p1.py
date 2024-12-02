from itertools import product

inp = range(271973, 785961)
total = 0

for nums in product(range(10), repeat=6):
    if (num := int("".join([str(n) for n in nums]))) in inp:
        pairs = [nums[i:i+2] for i in range(len(nums) - 1)]
        pairfound = any([pair[0] == pair[1] for pair in pairs])
        if tuple(sorted(nums)) == nums and pairfound:
            total += 1

print(f"Total: {total}")
