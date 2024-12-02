from itertools import product

with open("Input/2019day2input.txt") as inputfile:
    init = [int(n) for n in inputfile.readline().strip().split(",")]


def simulate(a, b, init):
    nums = init.copy()
    nums[1], nums[2] = a, b
    currindex = 0
    done = False
    while not done:
        if nums[currindex] not in [1, 2, 99]:
            print(f"Failed: opcode {nums[currindex]} at index {currindex} not found.")
            return None
        else:
            if nums[currindex] == 1:
                if type(nums[nums[currindex + 3]]) == int:
                    nums[nums[currindex + 3]] = nums[nums[currindex + 1]] + nums[nums[currindex + 2]]
            elif nums[currindex] == 2:
                if type(nums[nums[currindex + 3]]) == int:
                    nums[nums[currindex + 3]] = nums[nums[currindex + 1]] * nums[nums[currindex + 2]]
            else:
                done = True
        currindex += 4
    return nums[0]


target = 19690720
for a, b in product(range(100), repeat=2):
    if simulate(a, b, init) == target:
        print(f"a = {a}, b = {b} yields {target}.\nFinal answer: {100 * a + b}")
