from math import ceil
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
        # remainder = (reactionMultiple * numberProduced) - number
        # if molecule == "VRPVC" or molecule == "BHXH":
        #     print(f"making {number} {molecule} there are {remainder} spares, therefore adding to {spareMolecules[molecule]}")
        # try:
        #     spareMolecules[molecule] += remainder
        # except KeyError:
        #     if remainder:
        #         spareMolecules[molecule] = int(remainder)

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


with open("Input/2019day14testinput.txt") as inputfile:
    reactions = [[[tuple(molecule.split(" ")) for molecule in molecules.split(", ")] for molecules in line.strip().split(" => ")] for line in inputfile.readlines()]
reactions = [[dict([(molecule, int(number)) for number, molecule in molecules]) for molecules in reaction] for reaction in reactions]
reactions = dict([(list(product.keys())[0], (list(product.values())[0], reactants)) for reactants, product in reactions])

print(ans1 := getbasecost("FUEL", 1, reactions), {"VRPVC": 0, "BHXH": 0})
