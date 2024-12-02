with open(r"Input\2020day2.txt") as inputfile:
    inputlines = [line.strip().split(" ") for line in inputfile.readlines()]

processedinput = [(tuple([int(c) for c in data[0].split("-")]), data[1].replace(":", ""), data[2]) for data in inputlines]

num_valid = 0
for policy_range, policy_character, password in processedinput:
    in_password = password.count(policy_character)
    if policy_range[0] <= in_password <= policy_range[1]:
        num_valid += 1

print(f"Valid passwords: {num_valid}/{len(processedinput)}")
