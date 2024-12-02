genAstart = 883
genBstart = 879
genAfactor = 16807
genBfactor = 48271

def value(prevnum, factor):
    return ((prevnum * factor) % 2147483647)

genAprev = genAstart
genBprev = genBstart
totalcorrect = 0

def partone():
    for i in range(40000000):
        global genAprev
        global genBprev
        genAval, genBval = value(genAprev, genAfactor), value(genBprev, genBfactor)
        genAbinary, genBbinary = bin(genAval)[-16:], bin(genBval)[-16:]
        if genAbinary == genBbinary:
            totalcorrect += 1
        genAprev = genAval
        genBprev = genBval
        if not ((i + 1) % 100000):
            print("Completed " + str(i + 1) + " of 40000000 operations.")

    return totalcorrect

def parttwo():
    global genAprev
    global genBprev
    genAlist = []
    genBlist = []
    while (len(genAlist) < 5000000):
        genAval = value(genAprev, genAfactor)
        if not genAval % 4:
            genAlist.append(bin(genAval)[-16:])
        genAprev = genAval
    print("Generated A values.")
        
    while (len(genBlist) < 5000000):
        genBval = value(genBprev, genBfactor)
        if not genBval % 8:
            genBlist.append(bin(genBval)[-16:])
        genBprev = genBval
    print("Generated B values.")
    
    print("Commencing numcheck.")
    totalcorrect = 0
    for index, thing in enumerate(genAlist, 1):
        if thing == genBlist[index - 1]:
            totalcorrect += 1
        if not ((index) % 500000):
            print("Completed " + str(index) + " of 5000000 operations.")
    return totalcorrect
            
        
    
    
    
    


