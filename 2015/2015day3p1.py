with open("day3input.txt") as inputfile:
    inputstring = "".join([line.strip() for line in inputfile.readlines()])

movedict = {"^":"y+=1", ">":"x+=1", "<":"x-=1", "v":"y-=1"}

x = 0
y = 0
coords = [x, y]
visited = [[0, 0]]

for char in inputstring:
    exec(movedict[char])
    coords = [x, y]
    if not coords in visited:
        visited.append(list(coords))

print(len(visited))
