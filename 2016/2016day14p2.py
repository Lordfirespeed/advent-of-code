import hashlib

def triplechar(string):
    for index in range(0, len(string)-2):
        if string[index] == string[index+1] == string[index+2]:
            return string[index]
    return False

def quinchar(string):
    for index in range(0, len(string)-4):
        if string[index] == string[index+1] == string[index+2] == string[index+3] == string[index+4]:
            return string[index]
    return False

def md5hash(string):
    hashed = string
    for index in range(2017):
        newhash = hashlib.md5()
        newhash.update(hashed.encode())
        hashed = newhash.hexdigest().lower()
    return hashed

inputstring = "qzyelonm"
hashes = []
for index in range(0, 1001):
    hashes.append(md5hash(inputstring + str(index)))
print("Hashes 0-1000 generated.")

index = 1001
keys = []
while len(keys) < 64:
    currenthash = hashes[0]
    character = triplechar(currenthash)
    if character:
        quin = False
        for thousandindex in range(1, 1001):
            checkquinhash = hashes[thousandindex]
            quincharacter = quinchar(checkquinhash)
            if quincharacter == character:
                # print(index, character, thousandindex, quincharacter)
                quin = True
                break
        if quin:
            keys.append([int(index-1001), (thousandindex)])
            print("Found key, index " + str(index-1001) + ".")
    del hashes[0]
    hashes.append(md5hash(inputstring + str(index)))
    index += 1

print(keys[-1][0])

# for indexes in keys:
#     hasha = md5hash("qzyelonm" + str(indexes[0]))
#     hashb = md5hash("qzyelonm" + str(indexes[1]))
#     print(hasha, hashb)