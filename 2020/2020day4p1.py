with open(r"Input\2020day4.txt") as inputfile:
    inputstr = "".join([line.strip() + " " if line.strip() else "\n" for line in inputfile.readlines()])

passports_raw = [passport.strip().split(" ") for passport in inputstr.split("\n")]
passport_dicts = [dict([tuple(field.split(":")) for field in passport]) for passport in passports_raw]

required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
valid_passports = []

for passport in passport_dicts:
    if set(passport.keys()).issuperset(required_fields):
        valid_passports.append(passport)

print(f"Valid passports: {len(valid_passports)}/{len(passports_raw)}")
