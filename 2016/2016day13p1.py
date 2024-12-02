inputnum = 1364
target = (31, 39)
size = max(target) + 15

mapbool = {True:" ", False:"█"}
maze = []
# maze should be referenced in format maze[y][x]

for y in range(0, size+1):
    maze.append([])
    for x in range(0, size+1):
        value = x*x + 3*x + 2*x*y + y + y*y
        value += inputnum
        maze[y].append(mapbool[not (bin(value).count("1")) % 2])
        if x == target[0] and y == target[1]:
            maze[y][x] = "X"

with open("2016day13maze.txt", "w") as outputfile:
    for line in maze:
        outputfile.write("".join(line) + "\n")

currentloc = [1, 1]
# in format x, y
visited = []
tocheck = []
disttravelled = 0

tocheck.append([0, 0, list(currentloc)])
found = False
while not found:
    delindex = [location[2] for location in tocheck].index(currentloc)
    del tocheck[delindex]
    visited.append([list(currentloc), disttravelled])
    x = currentloc[0]
    y = currentloc[1]
    addtocheck = [[x, (y+1)], [(x+1), y], [x, (y-1)], [(x-1), y]]
    for location in addtocheck:
        if (maze[location[1]][location[0]] == "█") or location in [thing[0] for thing in visited]:
            pass
        elif location[0] < 0 or location[1] < 0 or location[0] > size-1 or location[1] > size-1:
            pass
        else:
            score = disttravelled + (target[0] - location[1]) + (target[1] - location[0])
            tocheck.append([int(score), int(disttravelled) + 1, list(location)])
    currentloc = min(tocheck[::-1])[2]
    disttravelled = min(tocheck[::-1])[1]
    if tuple(currentloc) == target:
        found = True
        print(disttravelled)
