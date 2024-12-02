import hashlib

inputstring = "ugkcyxxp"
index = 0
key = "________"
while "_" in key:
    newhash = hashlib.md5()
    newhash.update((inputstring + str(index)).encode())
    hashed = newhash.hexdigest()
    if hashed[:5] == "00000":
        validpos = [str(index) for index, char in enumerate(key) if char == "_"]
        pos = hashed[5]
        if pos in validpos:
            key = key[:int(pos)] + hashed[6] + key[int(pos)+1:]
            print(key)
    index += 1
