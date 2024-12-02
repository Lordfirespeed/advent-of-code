with open(r"Input\2020day15.txt") as inputfile:
    input_nums = [int(n) for n in inputfile.readlines()[0].split(",")]

turn = len(input_nums)
turns_spoken = {value: [index+1] for index, value in enumerate(input_nums[:-1])}
last_spoken_num = input_nums[-1]

while turn < 30_000_000:
    turn += 1

    if last_spoken_num not in turns_spoken.keys():
        turns_spoken[last_spoken_num] = []

    if len(turns_spoken[last_spoken_num]) >= 2:
        turns_spoken[last_spoken_num].pop(0)
    turns_spoken[last_spoken_num].append(turn-1)

    if last_spoken_num in turns_spoken.keys():
        try:
            last_spoken_num = turns_spoken[last_spoken_num][1] - turns_spoken[last_spoken_num][0]
        except IndexError:
            last_spoken_num = 0
    else:
        last_spoken_num = 0

print(f"Number spoken on the 30,000,000th turn: {last_spoken_num}")
