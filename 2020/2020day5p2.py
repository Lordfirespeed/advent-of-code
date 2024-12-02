with open(r"Input\2020day5.txt") as inputfile:
    passes = [line.strip() for line in inputfile.readlines()]


def interpolate(num1, num2):
    return int((num1+num2)/2)


def reduce(curr_range: tuple, chars: str):
    if curr_range[0] == curr_range[1]:
        return curr_range[0]
    else:
        if chars[0] == "F" or chars[0] == "L":
            # take lower half
            new_upper_bound = interpolate(curr_range[0], curr_range[1])
            return reduce((curr_range[0], new_upper_bound), chars[1:])
        elif chars[0] == "B" or chars[0] == "R":
            # take upper half
            new_lower_bound = interpolate(curr_range[0], curr_range[1]) + 1
            return reduce((new_lower_bound, curr_range[1]), chars[1:])
        else:
            print("UNEXPECTED CHARACTER")


def seat_id(row, column):
    return row * 8 + column


seat_ids = []
for seat in passes:
    row = reduce((0, 127), seat[:7])
    column = reduce((0, 7), seat[7:])
    seat_ids.append(seat_id(row, column))

all_seat_ids = range(min(seat_ids), max(seat_ids)+1)
missing_seat_ids = set(all_seat_ids) - set(seat_ids)

print(f"Your seat ID: {missing_seat_ids.pop()}")
