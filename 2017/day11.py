def initturtle():
    import turtle

    turtle.speed(10)
    movedist = 10
    turtle.mode("logo")
    turtle.ht()
    turtle.color("lime")

def n():
    turtle.seth(0)
    turtle.forward(movedist)
    turtle.dot(3)

def ne():
    turtle.seth(60)
    turtle.forward(movedist)
    turtle.dot(3)

def se():
    turtle.seth(120)
    turtle.forward(movedist)
    turtle.dot(3)

def s():
    turtle.seth(180)
    turtle.forward(movedist)
    turtle.dot(3)

def sw():
    turtle.seth(240)
    turtle.forward(movedist)
    turtle.dot(3)

def nw():
    turtle.seth(300)
    turtle.forward(movedist)
    turtle.dot(3)

def simplify():
    with open("day11input.txt") as file:
        inputlist = ((file.readlines()[0]).rstrip()).split(",")
    inputlist.sort()
    outputlist = []

    namount = inputlist.count("n")
    samount = inputlist.count("s")
    neamount = inputlist.count("ne")
    swamount = inputlist.count("sw")
    nwamount = inputlist.count("nw")
    seamount = inputlist.count("se")
    
    if namount > samount:
        for index in range(namount - samount):
            outputlist.append("n")
    else:
        for index in range(samount - namount):
            outputlist.append("s")

    if neamount > swamount:
        for index in range(neamount - swamount):
            outputlist.append("ne")
    else:
        for index in range(swamount - neamount):
            outputlist.append("sw")

    if nwamount > seamount:
        for index in range(nwamount - seamount):
            outputlist.append("nw")
    else:
        for index in range(seamount - nwamount):
            outputlist.append("se")
    
    inputlist = outputlist
    outputlist = []

    samount = inputlist.count("s")
    neamount = inputlist.count("ne")
    seamount = inputlist.count("se")

    seamount += samount
    neamount -= samount
    print(str(seamount + neamount))

    
