with open("day5input.txt") as inputfile:
    inputlist = [line.strip() for line in inputfile.readlines()]

import string
doubleletters = [(char*2) for char in string.ascii_lowercase]
vowels = list("aeiou")
badstrs = ["ab", "cd", "pq", "xy"]

good = []
for line in inputlist:
    linebadstrs = any([string in line for string in badstrs])
    linevowels =  sum(list(map(line.count, "aeiou"))) >= 3
    linedoubleletters = any([string in line for string in doubleletters])

    if linevowels and linedoubleletters and not linebadstrs:
        good.append(line)

print(len(good))
