with open("Input/2019day8input.txt") as inputfile:
    nums = inputfile.readline().strip()

xsize, ysize = 25, 6
size = xsize * ysize

layers = [[int(n) for n in nums[i:i+size]] for i in range(0, len(nums), size)]
zeros = [layer.count(0) for layer in layers]
zeros = list(zip(*list(zip(*enumerate(zeros)))[::-1]))
correctlayer = layers[min(zeros)[1]]
answer = correctlayer.count(1) * correctlayer.count(2)
print(answer)
