with open("2018day10input.txt") as inputfile:
    particles = [line.strip() for line in inputfile.readlines()]


def getdims(locations):
    xvals, yvals = zip(*locations)
    maxx, minx, maxy, miny = max(xvals), min(xvals), max(yvals), min(yvals)
    size = (maxx-minx) * (maxy-miny)
    return maxx, minx, maxy, miny, size


def simulate(time):
    global particles
    newparticles = []
    for particle in particles:
        newx = particle["position"][0] + (particle["velocity"][0] * time)
        newy = particle["position"][1] + (particle["velocity"][1] * time)
        newparticles.append((newx, newy))
    return newparticles


def display(locations):
    maxx, minx, maxy, miny, size = getdims(locations)
    lines = []
    for y in range(maxy, miny-1, -1):
        line = ""
        for x in range(minx, maxx+1):
            line += "#" if (x, y) in locations else " "
        lines.append(line)
    return lines


particles = [[variable.split("=") for variable in particle.split("> ")] for particle in particles]
particles = [dict([(varname, [int(v.strip()) for v in value[1:].replace(">", "").split(", ")]) for varname, value in particle]) for particle in particles]

currSize = getdims(simulate(0))[-1]
lastSize = currSize + 1
currTime = 0
while currSize < lastSize:
    lastSize = int(currSize)
    currTime += 1
    currSize = getdims(simulate(currTime))[-1]
currTime -= 1
print("\n".join(display(simulate(currTime))[::-1]))  # FBHKLEAG
print(currTime)
