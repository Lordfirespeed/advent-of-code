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


def get_capacity(bag_name):
    global tokenised_remove_s
    contains = tokenised_remove_s[bag_name]
    if contains == {}:
        return 1
    else:
        val = sum([(get_capacity(contained_bag) * number) for contained_bag, number in contains.items()]) + 1
        return val


print(f"Number of bags contained by shiny gold: {get_capacity('shiny gold bag') - 1}")
