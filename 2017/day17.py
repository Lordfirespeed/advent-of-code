def partone(stepnum):
    buffer = [0]
    currentpos = 0
    for insertnum in range(1, 2018):
        currentpos += stepnum
        currentpos %= len(buffer)
        buffer.insert((currentpos + 1), insertnum)
        currentpos += 1
        currentpos %= len(buffer)

    pos2017 = buffer.index(2017)
    pos2018 = ((pos2017 + 1) % len(buffer))
    print(buffer[pos2018])


def parttwo(stepnum):
    buffer = [0]
    currentpos = 0
    for insertnum in range(1, 50000000):
        currentpos += stepnum
        currentpos %= len(buffer)
        buffer.insert((currentpos + 1), insertnum)
        currentpos += 1
        currentpos %= len(buffer)
        if not insertnum % 1000000:
            print("Completed " + str(insertnum) + " of 50000000 insertions.")

    print(buffer[1])

