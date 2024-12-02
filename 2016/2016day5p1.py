import hashlib

inputstring = "ugkcyxxp"
index = 0
key = ""
while len(key) < 8:
    newhash = hashlib.md5()
    newhash.update((inputstring + str(index)).encode())
    hashed = newhash.hexdigest()
    if hashed[:5] == "00000":
        key = key + hashed[5]
        print(key)
    index += 1
