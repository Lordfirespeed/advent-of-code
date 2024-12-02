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
    newhash = hashlib.md5()
    newhash.update(string.encode())
    hashed = newhash.hexdigest().lower()
    return hashed

inputstring = "qzyelonm"
index = 0
keys = []
while len(keys) < 64:
    hashed = md5hash(inputstring + str(index))
    character = triplechar(hashed)
    if character:
        quin = False
        for thousandindex in range(index+1, index+1001):
            checkquinhash = md5hash(inputstring + str(thousandindex))
            quincharacter = quinchar(checkquinhash)
            if quincharacter == character:
                # print(index, character, thousandindex, quincharacter)
                quin = True
                break
        if quin:
            keys.append([int(index), (thousandindex)])
    index += 1

print(keys[-1][0])

# for indexes in keys:
#     hasha = md5hash("qzyelonm" + str(indexes[0]))
#     hashb = md5hash("qzyelonm" + str(indexes[1]))
#     print(hasha, hashb)