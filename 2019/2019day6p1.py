class Tree(object):
    def __init__(self, name, children=None, parent=None):
        if children is None:
            children = list()
        self.name = name
        self.children = children
        self.parent = parent
        self.depth = parent.depth + 1 if parent else 0

    def __str__(self):
        return self.name + ", " + str(self.children)

    def __repr__(self):
        return self.name

    def addchild(self, child):
        self.children.append(child)

    def getparent(self):
        return self.parent

    def getchildren(self):
        return self.children

    def getchild(self, name):
        try:
            return [child for child in self.children if (child.name == name if type(child) == Tree else False)][0]
        except IndexError:
            return None

    def getelement(self, name):
        if self.name == name:
            return self
        if found := self.getchild(name):
            return found
        else:
            for child in self.getchildren():
                if type(child) == Tree:
                    if found := child.recrgetchild(name):
                        return found
            return None

    def recrgetchildren(self):
        extra = []
        for child in (children := self.getchildren()):
            if type(child) == Tree:
                extra += child.recrgetchildren()
        return children + extra

    def copy(self):
        if any(trees := [type(child) == Tree for child in self.getchildren()]):
            return Tree(self.name, [child.copy() if tree else child for tree, child in zip(trees, self.getchildren())])
        else:
            return Tree(self, self.getchildren().copy())


with open("Input/2019day6input.txt") as inputfile:
    orbits = [line.strip().split(")") for line in inputfile.readlines()]

base = Tree("COM")
changed = True
while changed:
    changed = False
    for orbit in orbits:
        if orbiting := base.getelement(orbit[0]):
            if not orbiting.getchild(orbit[1]):
                orbiting.addchild(Tree(orbit[1], parent=orbiting))
                changed = True

orbits = base.recrgetchildren()
print(orbits)
total = sum([orbit.depth for orbit in orbits])
print(total)
