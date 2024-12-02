from itertools import combinations

with open(r"Input\2020day9test.txt") as inputfile:
    inputnums = [int(line.strip()) for line in inputfile.readlines()]

preamble_length = 5

curr_previous = inputnums[:preamble_length]
available_sums = [sum(a) for a in combinations(curr_previous, r=2)]

final_number = None

for number in inputnums[preamble_length:]:
    if number in available_sums:
        curr_previous.pop(0)
        available_sums = available_sums[preamble_length-1:]
        for index, other in enumerate(curr_previous):
            available_sums.insert(sum([preamble_length-2-r for r in range(index+1)])+index, number+other)  # did some maths for this
            # a preamble of len 25: first number -> 24 sums, second number -> 23 sums etc.
            # as we remove number index 0, we remove the first 24 sums from the available_sums
            # then, we insert numbers to the respective regions for each lower number
            # first number (index 0) goes to index 23 (as the region is of length 23)
            # second number (index 1) goes to index 23+22+1 (as the region is of length 23+22 and we have done one insertion)
            # third number (index 2) goes to index 23+22+21+2 (as the region is of length 23+22+21 and we have done 2 insertions)
            # etc. This can be generalised into sum([preamble_length-2-r] for r in range(index+1)]), or by sigma notation
        curr_previous.append(number)
    else:
        final_number = number
        break

print(f"First invalid: {final_number}")
