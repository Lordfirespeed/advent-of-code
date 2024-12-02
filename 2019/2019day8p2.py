with open("Input/2019day8input.txt") as inputfile:
    nums = inputfile.readline().strip()

xsize, ysize = 25, 6
size = xsize * ysize

layers = [[int(n) for n in nums[i:i+size]] for i in range(0, len(nums), size)]
layers = [[layer[n:n+xsize] for n in range(0, size, xsize)]for layer in layers]

render = [[3 for x in range(xsize)] for y in range(ysize)]
change = {0: " ", 1: "█", 2: " "}
for y in range(ysize):
    for x in range(xsize):
        layer = 0
        try:
            while layers[layer][y][x] == 2:
                layer += 1
        except IndexError:
            layer -= 1
        render[y][x] = change[layers[layer][y][x]]

print("\n".join(["".join([str(n) for n in row]) for row in render]))
