with open("Input/2019day2input.txt") as inputfile:
    nums = [int(n) for n in inputfile.readline().strip().split(",")]

if actual := True:
    nums[1], nums[2] = 12, 2

currindex = 0
done = False
while not done:
    if nums[currindex] not in [1, 2, 99]:
        print(f"Failed: opcode {nums[currindex]} at index {currindex} not found.")
    else:
        if nums[currindex] == 1:
            nums[nums[currindex + 3]] = nums[nums[currindex + 1]] + nums[nums[currindex + 2]]
        elif nums[currindex] == 2:
            nums[nums[currindex + 3]] = nums[nums[currindex + 1]] * nums[nums[currindex + 2]]
        else:
            done = True
    currindex += 4

print(nums[0])
