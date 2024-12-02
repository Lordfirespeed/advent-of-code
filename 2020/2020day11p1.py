with open(r"Input\2020day11.txt") as inputfile:
    input_arrangement = [list(line.strip()) for line in inputfile.readlines()]


class Conways_Seats:
    def __init__(self, initial_arrangement):
        self.arrangement = initial_arrangement
        self.current_iteration = 0
        self.stable = False

    def __repr__(self):
        arrangement_string = "\n".join(["".join(row) for row in self.arrangement])
        return f"Iteration: {self.current_iteration}\n{arrangement_string}"

    def get_adjacent_seats(self, x, y):
        if y < 0:
            y = len(self.arrangement) + y
        if x < 0:
            x = len(self.arrangement) + x
        seats = []
        for check_y in range(y-1, y+2):
            if 0 <= check_y < len(self.arrangement):
                row = self.arrangement[check_y]
                for check_x in range(x-1, x+2):
                    if 0 <= check_x < len(row):
                        if not (check_x == x and check_y == y):
                            seats.append(row[check_x])
        return seats

    def get_occupied(self):
        return [seat for row in self.arrangement for seat in row].count("#")

    def simulate(self):
        if not self.stable:
            changed = False
            new_arrangement = [row.copy() for row in self.arrangement]
            for yindex, row in enumerate(self.arrangement):
                for xindex, seat in enumerate(row):
                    occupied_adjacent = self.get_adjacent_seats(xindex, yindex).count("#")
                    if seat == "L" and occupied_adjacent == 0:
                        new_arrangement[yindex][xindex] = "#"
                        changed = True
                    elif seat == "#" and occupied_adjacent >= 4:
                        new_arrangement[yindex][xindex] = "L"
                        changed = True
            if not changed:
                self.stable = True
            self.current_iteration += 1
            self.arrangement = new_arrangement


station_seats = Conways_Seats(input_arrangement)
while not station_seats.stable:
    station_seats.simulate()

print(f"Occupied seats: {station_seats.get_occupied()}")
