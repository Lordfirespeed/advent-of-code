from itertools import permutations

with open("Input/2019day12input.txt") as inputfile:
    planets = [line.strip()[1:-1].split(", ") for line in inputfile.readlines()]

planets = [dict([tuple(var.split("=")) for var in planet]) for planet in planets]
planets = [{key: int(value) for key, value in zip(planet.keys(), planet.values())} for planet in planets]
planets = [(planet, {"x": 0, "y": 0, "z": 0}) for planet in planets]

seenBefore = []
time = 0
while planets not in seenBefore:
    seenBefore.append([(location.copy(), velocity.copy()) for location, velocity in planets])
    # [print(moon) for moon in planets]
    # print()
    for moonAIndex in range(len(planets)):
        for moonBIndex in range(moonAIndex + 1, len(planets)):
            moonA, moonB = planets[moonAIndex], planets[moonBIndex]
            for dimension in ("x", "y", "z"):
                if moonA[0][dimension] == moonB[0][dimension]:
                    pass
                elif moonA[0][dimension] < moonB[0][dimension]:
                    moonA[1][dimension] += 1
                    moonB[1][dimension] -= 1
                else:
                    moonA[1][dimension] -= 1
                    moonB[1][dimension] += 1
    for moon in planets:
        for dimension in ("x", "y", "z"):
            moon[0][dimension] += moon[1][dimension]
    time += 1
    if not time % 1_000_000:
        print(time)

print(time)
