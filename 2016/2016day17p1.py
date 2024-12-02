import hashlib

password = "rrrbmfta"
openmap = ["B", "C", "D", "E", "F"]


def md5hash(string):
    newhash = hashlib.md5()
    newhash.update(string.encode())
    hashed = newhash.hexdigest()
    return hashed


def doors(path):
    path = path.upper()
    hash = md5hash(password + path).upper()
    up = hash[0] in openmap
    down = hash[1] in openmap
    left = hash[2] in openmap
    right = hash[3] in openmap
    return [bool(up), bool(down), bool(left), bool(right)]


def generaterooms(location):
    addtotovisit = []
    unlockeddoors = doors(location[2])
    if unlockeddoors[0]:
        addtotovisit.append([int(location[0]), int(location[1])-1, (str(location[2]) + "U")])
    if unlockeddoors[1]:
        addtotovisit.append([int(location[0]), int(location[1])+1, (str(location[2]) + "D")])
    if unlockeddoors[2]:
        addtotovisit.append([int(location[0])-1, int(location[1]), (str(location[2]) + "L")])
    if unlockeddoors[3]:
        addtotovisit.append([int(location[0])+1, int(location[1]), (str(location[2]) + "R")])

    invalid = []
    for index, coordinates in enumerate([location[:2] for location in addtotovisit]):
        if max(coordinates) > 3 or min(coordinates) < 0:
            invalid.append(index)
    for index in invalid[::-1]:
        del addtotovisit[index]

    return addtotovisit



location = [0, 0, ""]
tovisit = []
exhausted = []
# locations in format x, y, path
tovisit
