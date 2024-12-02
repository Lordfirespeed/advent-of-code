from itertools import product

with open(r"Input\2020day17.txt") as inputfile:
    inputlines = [list(line.strip()) for line in inputfile.readlines()]


class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        if type(other) == Vector3:
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        elif type(other) == "int":
            return Vector3(self.x + other, self.y + other, self.z + other)
        else:
            raise TypeError(f"Cannot sum Vector3 and {type(other)}")


class Conway_3D:
    def __init__(self, zero_z_crosssection):
        self.grid = {0: zero_z_crosssection}
        self.iteration = 0

    def __repr__(self):
        arrangement_string = "\n".join([" " + "  ".join(["".join(xy_grid[x_index]) for z, xy_grid in sorted(list(self.grid.items()))]) for x_index in range(len(self.grid[0]))])
        return f"Iteration: {self.iteration}\n{arrangement_string}"

    def get_active_cells(self):
        return [cell for xy_grid in self.grid.values() for x_row in xy_grid for cell in x_row].count("#")

    def get_adjacent_cells(self, position: Vector3):
        cells = []
        for vector_nums in set(product([0, 1, -1], repeat=3)):
            if vector_nums != (0, 0, 0):
                check_pos = position + Vector3(*vector_nums)
                try:
                    cells.append(self.grid[check_pos.z][check_pos.y][check_pos.x])
                except IndexError:
                    cells.append(".")
                except KeyError:
                    cells.append(".")
        return cells

    def get_active_cells_range(self):
        minx, maxx = None, None
        miny, maxy = None, None
        minz, maxz = None, None
        for z, xy_grid in self.grid.items():
            for y, x_row in enumerate(xy_grid):
                for x, cell in enumerate(x_row):
                    if cell == "#":
                        minx = x if (minx is None) or x < minx else minx
                        maxx = x if (maxx is None) or x > maxx else maxx

                        miny = y if (miny is None) or y < miny else miny
                        maxy = y if (maxy is None) or y > maxy else maxy

                        minz = z if (minz is None) or z < minz else minz
                        maxz = z if (maxz is None) or z > maxz else maxz

        return {"X": (minx, maxx), "Y": (miny, maxy), "Z": (minz, maxz)}

    def correct_grid_size(self):
        grid_ranges = self.get_active_cells_range()
        self.grid = {z: xy_grid for z, xy_grid in self.grid.items() if grid_ranges["Z"][0] <= z <= grid_ranges["Z"][1]}

        old_x_size, old_y_size = grid_ranges["X"][1] - grid_ranges["X"][0] + 1, grid_ranges["Y"][1] - grid_ranges["Y"][0] + 1

        blank_x_row = ["."] * (old_x_size + 2)
        for z, xy_grid in self.grid.items():
            self.grid[z] = [["."] + x_row[grid_ranges["X"][0]:grid_ranges["X"][1]+1] + ["."] for x_row in xy_grid[grid_ranges["Y"][0]:grid_ranges["Y"][1]+1]]

            self.grid[z].insert(0, blank_x_row.copy())
            self.grid[z].append(blank_x_row.copy())

        blank_xy_grid = [["." for x in range(old_x_size+2)] for y in range(old_y_size+2)]
        self.grid[grid_ranges["Z"][0]-1] = [line.copy() for line in blank_xy_grid]
        self.grid[grid_ranges["Z"][1]+1] = [line.copy() for line in blank_xy_grid]

    def simulate(self):
        self.correct_grid_size()
        new_grid = {z: [x_row.copy() for x_row in xy_grid] for z, xy_grid in self.grid.items()}
        for z_index, xy_grid in self.grid.items():
            for y_index, x_row in enumerate(xy_grid):
                for x_index, cell in enumerate(x_row):
                    active_adjacent = self.get_adjacent_cells(Vector3(x_index, y_index, z_index)).count("#")
                    if cell == "#":
                        if not (2 <= active_adjacent <= 3):
                            new_grid[z_index][y_index][x_index] = "."
                    elif cell == ".":
                        if active_adjacent == 3:
                            new_grid[z_index][y_index][x_index] = "#"

        self.iteration += 1
        self.grid = new_grid


simulator = Conway_3D(inputlines)
print(simulator)
for i in range(6):
    simulator.simulate()
    print(simulator)

print(f"Number of active cells after 6 cycles: {simulator.get_active_cells()}")
