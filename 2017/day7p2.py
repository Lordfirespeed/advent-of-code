def getweight(name):
    with open("day7input.txt") as file:
        # Open file
        for linenum, line in enumerate(file.readlines(), 1):
            # for line in the file
            if ((line.rstrip())[:line.index(" ")]) == name:
                # if the name of the 'program' in the 'stack' is the name specified

                vallist = (line.rstrip()).split(" ")
                weight = vallist[1]
                weight = weight.replace("(", "")
                weight = weight.replace(")", "")
                weight = int(weight)
                # get the weight of the standalone program and trim parentheses
                
                if not "->" in line.rstrip():
                    # if the 'program' doesn't have any 'programs' on top of it
                    return weight
                    # return the weight of that standalone program
                    
                else:
                    # if the 'program' does have 'programs' on top of it
                    stackedprograms = (line.rstrip()[(line.index("-> ") + 3):]).split(", ")
                    # trim the line and get a list of the 'programs' on top
                    stackedweights = []
                    for program in stackedprograms:
                        stackedweights.append(getweight(program))
                    # get the weights of the stacked programs and append to a list
                    totalweight = weight + sum(stackedweights)
                    # assign the total weight of the 'program' to it's weight plus weights on top of it
                    return totalweight
                    # return the total weight of the 'program', including stacked 'programs'

def checkequal(iterable):
    return len(set(iterable)) <= 1

def checkweight(name):
    with open("day7input.txt") as file:
        # Open file
        for linenum, line in enumerate(file.readlines(), 1):
            # for line in the file
            if ((line.rstrip())[:line.index(" ")]) == name:
                # if the name of the 'program' in the 'stack' is the name specified
                stackedprograms = (line.rstrip()[(line.index("-> ") + 3):]).split(", ")
                # create a list of stacked 'programs'
                stackedweights = []
                for program in stackedprograms:
                    stackedweights.append(getweight(program))
                # get the weights of the 'programs'
                weightsequal = checkequal(stackedweights)
                # check the weights of the stacked 'programs' are equal. return true if so
                return weightsequal
                # return the value

def findwrong():
    with open("day7input.txt") as file:
        # Open file
        for linenum, line in enumerate(file.readlines(), 1):
            # for line in the file
            if "-> " in line.rstrip():
                # if the 'program' has stacked 'programs'
                programname = ((line.rstrip())[:line.index(" ")])
                # get the 'program' name from the line
                programok = checkweight(programname)
                if not programok:
                    # if one of the 'program's stacks are incorrect
                    print("One of '" + programname +  "'s' stacks are incorrect.")
                    stackedprograms = (line.rstrip()[(line.index("-> ") + 3):]).split(", ")
                    print(stackedprograms)
                    # get the stacked 'programs' and tell the user which 'program' has bad stacks
                    stackedweights = []
                    for program in stackedprograms:
                        stackedweights.append(getweight(program))
                    print(stackedweights)
                    # print the weights of each 'program' relative to the previously printed list
                    
                   
