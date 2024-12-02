names = []
values = []
allvalues = []

with open("day8input.txt") as file:
    for linenum, line in enumerate(file.readlines(), 1):
        action, condition = (line.rstrip()).split(" if ")
        actionname = action[:action.index(" ")]
        conditionname = condition[:condition.index(" ")]
        if not actionname in names:
            names.append(actionname)
            values.append(0)
        if not conditionname in names:
            names.append(conditionname)
            values.append(0)
        conditionindex = names.index(conditionname)
        condition = condition.replace(conditionname, str(values[conditionindex]))
        if eval(condition):
            actionindex = names.index(actionname)
            if "inc" in action:
                values[actionindex] = values[actionindex] + int((action.split(" "))[-1])
            else:
                values[actionindex] = values[actionindex] - int((action.split(" "))[-1])
            allvalues.append(values[actionindex])

minimumindex = values.index(min(values))
minimumname = names[minimumindex]
print("minimum is: " + minimumname, str(min(values)))

maximumindex = values.index(max(values))
maximumname = names[maximumindex]
print("maximum is: " + maximumname, str(max(values)))

print("maximum all time is: " + str(max(allvalues)))

print(values)
print(names)
