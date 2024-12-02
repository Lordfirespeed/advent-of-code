with open("2018day13input.txt") as inputfile:
    inputlines = [line.strip() for line in inputfile.readlines()]

initial = inputlines[0].replace("initial state: ", "")
rules = dict([[line[0:5], line[9]] for line in inputlines[2:]])

current = dict([[i, initial[i]] for i in range(len(initial))])
print("0: " + "".join([current[i] for i in current]))
for generation in range(1, 21):
    while current[min(current)] == ".":
        del current[min(current)]
    while current[max(current)] == ".":
        del current[max(current)]
    [exec("current[i]='.'") for i in range(min(current)-5, min(current))]
    [exec("current[i]='.'") for i in range(max(current)+1, max(current)+6)]
    new = dict(current)
    for index in range(min(current)+2, len(current)-2):
        try:
            new[index] = rules["".join([current[i] for i in range(index-2, index+3)])]
        except KeyError:
            new[index] = "."

    current = dict(new)
    print(str(generation)+": " + "".join([current[i] for i in range(min(current), max(current)+1)]))

end = dict(current)
result = sum(i for i in range(min(end), max(end)+1) if end[i] == "#")
print(result)