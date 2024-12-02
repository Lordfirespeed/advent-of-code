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

invalid = []

for ticket in all_tickets:
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
            invalid.append(value)

print(f"Ticket scanning error rate: {sum(invalid)}")
