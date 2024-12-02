with open(r"Input\2020day16.txt") as inputfile:
    inputlines = [line.strip() for line in inputfile.readlines()]


def get_ranges_from_string(string):
    string_ranges = string.split(" or ")
    return [[int(n) for n in string_range.split("-")] for string_range in string_ranges]


your_ticket_index = inputlines.index("your ticket:")
nearby_tickets_index = inputlines.index("nearby tickets:")

rules = inputlines[0:your_ticket_index-1]
your_ticket = inputlines[your_ticket_index+1]
nearby_tickets = inputlines[nearby_tickets_index+1:]

rules = [rule.split(": ") for rule in rules]
rules = {rule[0]: get_ranges_from_string(rule[1]) for rule in rules}

all_tickets = [your_ticket] + nearby_tickets
all_tickets = [[int(n) for n in ticket.split(",")] for ticket in all_tickets]

# remove invalid tickets
to_remove_indexes = []

for ticket_index, ticket in enumerate(all_tickets):
    for value in ticket:
        valid = False
        for rule, ranges in rules.items():
            for range_values in ranges:
                if range_values[0] <= value <= range_values[1]:
                    valid = True
                    break
            if valid:
                break
        if not valid:
            to_remove_indexes.append(ticket_index)
            break

for ticket_index in to_remove_indexes[::-1]:
    all_tickets.pop(ticket_index)

# now iterate through valid tickets
all_fields_set = set(rules.keys())
possible = [all_fields_set.copy() for field in all_tickets[0]]

for ticket in all_tickets:
    for field_index, value in enumerate(ticket):
        valid = False
        for rule, ranges in rules.items():
            if not (ranges[0][0] <= value <= ranges[0][1] or ranges[1][0] <= value <= ranges[1][1]):
                try:
                    possible[field_index].remove(rule)
                except KeyError:
                    pass

locked = {}
changed = True
while len(locked) < len(possible) and changed:
    changed = False
    for index, possible_fields_at_index_set in enumerate(possible):
        if len(possible_fields_at_index_set) == 1:
            locked[index] = possible_fields_at_index_set.pop()
    for possible_fields_at_index_set in possible:
        for locked_item in locked.values():
            if locked_item in possible_fields_at_index_set:
                possible_fields_at_index_set.remove(locked_item)
                changed = True

your_ticket = [int(n) for n in your_ticket.split(",")]

num = 1
for field_index, field_name in locked.items():
    if "departure" in field_name:
        num_on_your_ticket = your_ticket[field_index]
        num *= num_on_your_ticket

print(f"Product of 'Departure' numbers: {num}")
