with open("day3input.txt") as inputfile:
    inputstring = "".join([line.strip() for line in inputfile.readlines()])

movedict = {"^":"y+=1", ">":"x+=1", "<":"x-=1", "v":"y-=1"}

coords1 = [0, 0]
coords2 = [0, 0]
visited = [[0, 0]]

for index in range(0, len(inputstring), 2):
    x, y = coords1
    exec(movedict[inputstring[index]])
    coords1 = [x, y]

    x, y = coords2
    exec(movedict[inputstring[index+1]])
    coords2 = [x, y]

    if not coords1 in visited:
        visited.append(list(coords1))
    if not coords2 in visited:
        visited.append(list(coords2))

print(len(visited))
