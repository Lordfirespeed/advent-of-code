inputdata = [4, 192]  # puzzle input is 471 (players), 72026 (last marble's worth)

totalmarbles = inputdata[1]
players = inputdata[0]
playerscores = [0 for playerno in range(players+1)]

allmarbles = [marbleindex for marbleindex in range(0, totalmarbles+1)]
marblecircle = [0]

nextmarbleno = 1
currentmarbleindex = 0
while nextmarbleno < totalmarbles:
    for player in range(1, players+1):
        if nextmarbleno > totalmarbles:
            break

        if not nextmarbleno % 23 == 0:
            insertmarbleindex = (currentmarbleindex + 2) % len(marblecircle)
            marblecircle.insert(insertmarbleindex, nextmarbleno)
            currentmarbleindex = insertmarbleindex
        else:
            playerscores[player] += nextmarbleno
            removemarbleindex = currentmarbleindex - 7
            if removemarbleindex < 0:
                removemarbleindex = removemarbleindex + len(marblecircle)
            else:
                removemarbleindex = removemarbleindex % len(marblecircle)
            playerscores[player] += marblecircle[removemarbleindex]
            del marblecircle[removemarbleindex]
            currentmarbleindex = removemarbleindex
        print(player, marblecircle)
        nextmarbleno += 1
        if nextmarbleno % 10000 == 0:
            print(nextmarbleno, "/", totalmarbles)

print(playerscores[1:])
print(max(playerscores))
