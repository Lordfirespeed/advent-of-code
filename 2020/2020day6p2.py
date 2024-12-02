with open(r"Input\2020day6.txt") as inputfile:
    inputstr = "".join([line.strip() + "\n" if line.strip() else "\n" for line in inputfile.readlines()])

groups = inputstr.split("\n\n")
responses = [group.strip().split("\n") for group in groups]

summarised_responses = []

for group_responses in responses:
    group_response_sets = [set(list(response)) for response in group_responses]
    group_set = group_response_sets[0]
    if len(group_response_sets) > 1:
        group_set.intersection_update(*group_response_sets[1:])
    summarised_responses.append("".join(sorted(group_set)))

print(f"Total sum of summarised positive responses: {sum([len(summarised) for summarised in summarised_responses])}")
