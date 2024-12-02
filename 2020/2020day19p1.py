import re

with open(r"Input\2020day19.txt") as inputfile:
    inputlines = [line.strip() for line in inputfile.readlines()]

blank_line_index = inputlines.index("")
inputrules = inputlines[:blank_line_index]
inputmessages = inputlines[blank_line_index+1:]

resolved_rule_patterns = {}

rule_colon_indexes = [rule.index(":") for rule in inputrules]

raw_rules = [(int(rule[:colon_index]), [match_option.strip().split(" ") for match_option in rule[colon_index+2:].split("|")]) for rule, colon_index in zip(inputrules, rule_colon_indexes)]
raw_rules = {rule_index: ([[int(n) for n in match_option] for match_option in rule] if rule[0][0][0] != "\"" else rule) for rule_index, rule in raw_rules}

total_rules = len(raw_rules)

while len(resolved_rule_patterns) != total_rules:
    to_pop = []
    for rule_index, rule in raw_rules.items():
        if type(rule[0][0]) == str:
            resolved_rule_patterns[rule_index] = rule[0][0][1:-1]
            to_pop.append(rule_index)
        elif set([n for match_option in rule for n in match_option]).issubset(set(resolved_rule_patterns.keys())):
            pattern = "|".join(["".join([resolved_rule_patterns[rule_index] for rule_index in match_option]) for match_option in rule])
            if len(rule) > 1:
                pattern = "(" + pattern + ")"
            resolved_rule_patterns[rule_index] = pattern
            to_pop.append(rule_index)

    for rule_index in to_pop[::-1]:
        raw_rules.pop(rule_index)

matches_zero_rule = [message for message in inputmessages if re.fullmatch(resolved_rule_patterns[0], message)]
print(f"Number of messages that completely match rule zero: {len(matches_zero_rule)}")
