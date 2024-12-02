with open(r"Input\2020day7.txt") as inputfile:
    inputlines = [line.strip()[:-1] for line in inputfile.readlines()]

starting_key_value = [line.split(" contain ") for line in inputlines]
split_value = [(bag_key, value.split(", ")) for bag_key, value in starting_key_value]
split_contained_bags = [(bag_key, [bag.split(" ") for bag in contained_bags]) for bag_key, contained_bags in split_value]
tokenised_bags = dict([(bag_key, dict([(" ".join(bag[1:]), bag[0]) for bag in contained_bags])) for bag_key, contained_bags in split_contained_bags])
tokenised_remove_s = {}
for bag_key, contained_bags in tokenised_bags.items():
    bag_key = bag_key[:-1]
    if "no" in contained_bags.values():
        tokenised_remove_s[bag_key] = {}
    else:
        tokenised_remove_s[bag_key] = dict([((bag if int(num) == 1 else bag[:-1]), int(num)) for bag, num in contained_bags.items()])

can_contain_gold = ["shiny gold bag"]
changed = True
while changed:
    changed = False
    for bag, can_contain in tokenised_remove_s.items():
        if bag not in can_contain_gold:
            for check_can_contain_gold in can_contain_gold:
                if check_can_contain_gold in can_contain.keys():
                    can_contain_gold.append(bag)
                    changed = True
                    break

print(f"Bags that can contain shiny gold: {len(can_contain_gold) - 1}")