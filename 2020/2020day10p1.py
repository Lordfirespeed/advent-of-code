with open(r"Input\2020day10.txt") as inputfile:
    adapters = [int(n.strip()) for n in inputfile.readlines()]

adapters = sorted(adapters)
adapters.append(adapters[-1]+3)
adapters.insert(0, 0)

pairs_of_adapters = list(zip(adapters[:-1], adapters[1:]))

onejolts = [pair[1] - pair[0] == 1 for pair in pairs_of_adapters].count(True)
threejolts = [pair[1] - pair[0] == 3 for pair in pairs_of_adapters].count(True)

print(f"Product of one-jolt diffs and three-jolt diffs: {onejolts * threejolts}")
