with open("day16input.txt") as fileinput:
    line = fileinput.readline()
    line = line.rstrip()
    inputlist = line.split(",")

from string import ascii_lowercase
dancers = list(ascii_lowercase[:16])

for repetitions in range(1, 1_000_000_000):
    for command in inputlist:
        # print("".join(dancers), command)
        if command[0] == "s":
            # spin
            spinamount = int(command[1:])
            tomove = dancers[-spinamount:]
            dancers = dancers[:-spinamount]
            dancers = tomove + dancers
            
        elif command[0] == "x":
            # exchange
            indexA, indexB = (command[1:]).split("/")
            indexA, indexB = int(indexA), int(indexB)
            dancers[indexA], dancers[indexB] = dancers[indexB], dancers[indexA]
            
        elif command[0] == "p":
            # partner swap
            dancerA, dancerB = (command[1:]).split("/")
            indexA, indexB = dancers.index(dancerA), dancers.index(dancerB)
            dancers[indexA], dancers[indexB] = dancers[indexB], dancers[indexA]

    if repetitions == 1:
        print("".join(dancers))

    if not repetitions % 1000:
        print("Completed " + str(repetitions) + " of 1000000000 repetitions")

print("".join(dancers))
