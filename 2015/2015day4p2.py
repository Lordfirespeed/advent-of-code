import hashlib

inputstring = "bgvyzdsv"

index = 0
found = False
while not found:
    newhash = hashlib.md5()
    newhash.update((inputstring + str(index)).encode())
    hashed = newhash.hexdigest()
    if hashed[:6] == "000000":
        found = True
        print(index)
        break
    index += 1
