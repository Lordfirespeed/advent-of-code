with open(r"Input\2020day10test2.txt") as inputfile:
    adapters = [int(n.strip()) for n in inputfile.readlines()]

adapters = sorted(adapters)
adapters.append(adapters[-1]+3)
adapters.insert(0, 0)


def get_arrangements(adapters):
    arrangements = 1
    ways_of_deleting = [0 for adapter in adapters]
    index = 0
    while index < len(adapters) - 3:
        adapter = adapters[index]
        if len(adapters) - index >= 4 and adapters[index+3] == adapter + 3:
            ways_of_deleting[index+1] = 2 * (arrangements - ways_of_deleting[index])
            ways_of_deleting[index+2] = ways_of_deleting[index+1]
            arrangements = ways_of_deleting[index] + (arrangements - ways_of_deleting[index]) * 4
            index += 2

        elif len(adapters) - index >= 3 and adapters[index+2] <= adapter + 3:
            ways_of_deleting[index+1] = arrangements - ways_of_deleting[index]
            arrangements = ways_of_deleting[index] + (arrangements - ways_of_deleting[index]) * 2
            index += 1

        else:
            index += 1
    print(ways_of_deleting)
    return arrangements


print(f"Number of valid arrangments: {get_arrangements(adapters)}")
