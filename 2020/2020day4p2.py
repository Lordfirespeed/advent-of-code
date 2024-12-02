with open(r"Input\2020day4.txt") as inputfile:
    inputstr = "".join([line.strip() + " " if line.strip() else "\n" for line in inputfile.readlines()])

passports_raw = [passport.strip().split(" ") for passport in inputstr.split("\n")]
passport_dicts = [dict([tuple(field.split(":")) for field in passport]) for passport in passports_raw]

required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
valid_hcl_chars = set("0123456789abcdef")
valid_ecl = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


def validate_field(field: str, value: str):
    try:
        if field == "byr":
            return 1920 <= int(value) <= 2002
        elif field == "iyr":
            return 2010 <= int(value) <= 2020
        elif field == "eyr":
            return 2020 <= int(value) <= 2030
        elif field == "hgt":
            if value[-2:] == "cm":
                return 150 <= int(value[:-2]) <= 193
            elif value[-2:] == "in":
                return 59 <= int(value[:-2]) <= 76
            else:
                return False
        elif field == "hcl":
            return value[0] == "#" and len(value) == 7 and set(value[1:]).issubset(valid_hcl_chars)
        elif field == "ecl":
            return value in valid_ecl
        elif field == "pid":
            return len(value) == 9 and value.isnumeric()
        elif field == "cid":
            return True
        else:
            return False

    except:
        print("UNHANDLED! assuming invalid...")
        print(f"{field}: {value}")
        return False


valid_passports = []

for passport in passport_dicts:
    if set(passport.keys()).issuperset(required_fields) and all([validate_field(field, value) for field, value in passport.items()]):
        valid_passports.append(passport)

print(f"Valid passports: {len(valid_passports)}/{len(passports_raw)}")
