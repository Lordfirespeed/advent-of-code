from math import ceil, log10
debug = False


def getbasecost(molecule, number, reactions, spareMolecules={}):
    global debug
    reaction = reactions[molecule]
    if number == 0:
        return 0, spareMolecules
    elif tuple(reaction[1].keys()) == ("ORE",):
        numberProduced = reaction[0]
        reactionMultiple = ceil(number / numberProduced)

        singleCost = reaction[1]["ORE"]
        orePrice = reactionMultiple * singleCost

        print(f"making {numberProduced} {molecule} requires {singleCost} ore, {number} is needed, the cost is {orePrice}") if debug else None

        return orePrice, spareMolecules

    else:
        totalore = 0
        numberProduced = reaction[0]
        reactionMultiple = ceil(number / numberProduced)
        for reactantMolecule in reaction[1].keys():
            reactantReaction = reactions[reactantMolecule]
            reactantMoleculeRequired = reactionMultiple * reaction[1][reactantMolecule]
            reactantMoleculeProduced = reactantReaction[0]
            origReactantRequired = int(reactantMoleculeRequired)

            print(f"making {molecule} requires {reactantMoleculeRequired} {reactantMolecule}.") if debug else None
            try:
                spareReactantMolecules = spareMolecules[reactantMolecule]
                print(f"but there are {spareReactantMolecules} spares") if debug else None
                if spareReactantMolecules == 0:
                    pass
                elif spareReactantMolecules == reactantMoleculeRequired:
                    reactantMoleculeRequired = 0
                elif spareReactantMolecules > reactantMoleculeRequired:
                    reactantMoleculeRequired = 0
                else:
                    reactantMoleculeRequired -= spareReactantMolecules
            except KeyError:
                print(f"There are no spare molecules.") if debug else None
                pass

            reactantReactionMultiple = ceil(reactantMoleculeRequired / reactantMoleculeProduced)

            reactantTotal = reactantReactionMultiple * reactantMoleculeProduced
            print("REACTANT TOTAL 0") if reactantTotal == 0 and debug else None
            reactantRemainder = reactantTotal - reactantMoleculeRequired

            print(f"making {molecule} requires {reactantMoleculeRequired} {reactantMolecule}.") if debug else None
            print(f"{reactantMoleculeProduced} can be made at once, {reactantTotal} made total, so {reactantRemainder} would be wasted") if debug else None
            if reactantTotal == 0:
                spareMolecules[reactantMolecule] -= origReactantRequired
            else:
                spareMolecules[reactantMolecule] = int(reactantRemainder)
            print(spareMolecules) if debug else None
            reactantTotalOre, otherRemainder = getbasecost(reactantMolecule, reactantTotal, reactions, spareMolecules)
            spareMolecules.update(otherRemainder)
            print(f"Adding {reactantMolecule} total {reactantTotalOre} to molecule {molecule} * {number} total {totalore}") if debug else None
            totalore += reactantTotalOre
            print(f"Result {totalore}") if debug else None
            print() if debug else None
        return totalore, spareMolecules


def makemax(ore, molecule, reactions, spareMolecules={}):
    currOre, newSpareMolecules = int(ore), spareMolecules.copy()
    made, cost = 0, 0
    maxpow = int(log10(ore))
    powersTen = [10 ** i for i in range(maxpow, -1, -1)]
    for powersTenIndex in range(len(powersTen)):
        while cost <= currOre:
            currOre, currSpareMolecules = currOre - cost, newSpareMolecules.copy()
            cost, newSpareMolecules = getbasecost(molecule, powersTen[powersTenIndex], reactions, currSpareMolecules.copy())
            made += powersTen[powersTenIndex]
        newSpareMolecules = currSpareMolecules.copy()
        cost = 0

    made -= sum(powersTen)
    return made


with open("Input/2019day14input.txt") as inputfile:
    reactions = [[[tuple(molecule.split(" ")) for molecule in molecules.split(", ")] for molecules in line.strip().split(" => ")] for line in inputfile.readlines()]
reactions = [[dict([(molecule, int(number)) for number, molecule in molecules]) for molecules in reaction] for reaction in reactions]
reactions = dict([(list(product.keys())[0], (list(product.values())[0], reactants)) for reactants, product in reactions])

print(ans := getbasecost("FUEL", 1, reactions), {"VRPVC": 0, "BHXH": 0})
print(ans2 := makemax(1_000_000_000_000, "FUEL", reactions))
