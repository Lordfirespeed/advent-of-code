def array(twodlist):
    return [list(thing) for thing in twodlist]

inputnum = 1364
size = 55

mapbool = {True:" ", False:"X"}
maze = []
# maze should be referenced in format maze[y][x]

for y in range(0, size+1):
    maze.append([])
    for x in range(0, size+1):
        value = x*x + 3*x + 2*x*y + y + y*y
        value += inputnum
        maze[y].append(mapbool[not (bin(value).count("1")) % 2])

with open("2016day13maze.txt", "w") as outputfile:
    for line in maze:
        outputfile.write(("".join(line) + "\n"))

alllocations = [[x, y] for x in range(size+1) for y in range(size+1) if not maze[y][x] == "X"]

# in format x, y
visited = [[1, 1, 0]]
prevvisited = []
tocheck = []
disttravelled = 0

complete = False
while not complete:
    prevvisited = array(visited)
    if [location[:2] for location in visited] == alllocations:
        complete = True
    tocheck = [newplaces for places in [[[x+1, y, dist+1], [x, y-1, dist+1], [x-1, y, dist+1], [x, y+1, dist+1]] for x, y, dist in visited] for newplaces in places]
    tocheck = [place for place in tocheck if (0 <= place[0] <= size) and (0 <= place[1] <= size)]
    tocheck = [place for place in tocheck if not maze[place[1]][place[0]] == "X"]
    for location in tocheck:
        visitedlocations = [visitedloc[:2] for visitedloc in visited]
        if location[:2] in visitedlocations:
            visitedindex = visitedlocations.index(location[:2])
            if location[2] < visited[visitedindex][2]:
                visited[visitedindex][2] = location[2]
        else:
            visited.append(location)
    if visited == prevvisited:
        complete = True

print(len([location for location in visited if location[2] <= 50]))