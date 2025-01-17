from itertools import product

with open(r"Input\2020day17.txt") as inputfile:
    inputlines = [list(line.strip()) for line in inputfile.readlines()]


class Vector4:
    def __init__(self, x, y, z, a):
        self.x = x
        self.y = y
        self.z = z
        self.a = a

    def __add__(self, other):
        if type(other) == Vector4:
            return Vector4(self.x + other.x, self.y + other.y, self.z + other.z, self.a + other.a)
        elif type(other) == "int":
            return Vector4(self.x + other, self.y + other, self.z + other, self.a + other)
        else:
            raise TypeError(f"Cannot sum Vector4 and {type(other)}")


class Conway_4D:
    def __init__(self, zero_az_crosssection):
        self.grid = {0: {0: zero_az_crosssection}}
        self.iteration = 0

    def __repr__(self):
        a_ordered_grid_items = list(self.grid.items())
        a_ordered_grid_items.sort()

        indent = " "
        z_slice_separator = "  "
        a_slice_separator = "\n\n"

        def present_row_of_z_slice(z_slice: dict[int, str], x_index: int) -> str:
            return "".join(z_slice[x_index])

        def present_row_of_all_z_slices(a_slice: dict[int, dict[int, str]], x_index: int) -> str:
            z_ordered_grid_items = sorted(list(a_slice.items()))
            z_slice_rows = (present_row_of_z_slice(z_slice, x_index) for z_index, z_slice in z_ordered_grid_items)
            return indent + z_slice_separator.join(z_slice_rows)

        def present_all_z_slices(a_slice: dict[int, dict[int, str]]) -> str:
            grid_x_size = len(a_slice[0])
            return "\n".join(present_row_of_all_z_slices(a_slice, x_index) for x_index in range(grid_x_size))

        def present_all_a_slices() -> str:
            return a_slice_separator.join(present_all_z_slices(a_slice) for a_index, a_slice in a_ordered_grid_items)

        arrangement_string = present_all_a_slices()
        return f"Iteration: {self.iteration}\n{arrangement_string}"

    def get_active_cells(self):
        return [
            cell for xyz_grid in self.grid.values() for xy_grid in xyz_grid.values() for x_row in xy_grid for cell in x_row
        ].count("#")

    def get_adjacent_cells(self, position: Vector4):
        cells = []
        for vector_nums in set(product([0, 1, -1], repeat=4)):
            if vector_nums != (0, 0, 0, 0):
                check_pos = position + Vector4(*vector_nums)
                try:
                    cells.append(self.grid[check_pos.a][check_pos.z][check_pos.y][check_pos.x])
                except IndexError:
                    cells.append(".")
                except KeyError:
                    cells.append(".")
        return cells

    def get_active_cells_range(self):
        minx, maxx = None, None
        miny, maxy = None, None
        minz, maxz = None, None
        mina, maxa = None, None
        for a, xyz_grid in self.grid.items():
            for z, xy_grid in xyz_grid.items():
                for y, x_row in enumerate(xy_grid):
                    for x, cell in enumerate(x_row):
                        if cell == "#":
                            minx = x if (minx is None) or x < minx else minx
                            maxx = x if (maxx is None) or x > maxx else maxx

                            miny = y if (miny is None) or y < miny else miny
                            maxy = y if (maxy is None) or y > maxy else maxy

                            minz = z if (minz is None) or z < minz else minz
                            maxz = z if (maxz is None) or z > maxz else maxz

                            mina = a if (mina is None) or a < mina else mina
                            maxa = a if (maxa is None) or a > maxa else maxa

        return {"X": (minx, maxx), "Y": (miny, maxy), "Z": (minz, maxz), "A": (mina, maxa)}

    def correct_grid_size(self):
        grid_ranges = self.get_active_cells_range()

        old_x_size, old_y_size = grid_ranges["X"][1] - grid_ranges["X"][0] + 1, grid_ranges["Y"][1] - grid_ranges["Y"][
            0] + 1
        blank_x_row = ["."] * (old_x_size + 2)
        blank_xy_grid = [blank_x_row.copy() for _ in range(old_y_size + 2)]

        self.grid = {a: xyz_grid for a, xyz_grid in self.grid.items() if
                     grid_ranges["A"][0] <= a <= grid_ranges["A"][1]}

        self.grid[grid_ranges["A"][0] - 1] = {z: [line.copy() for line in blank_xy_grid] for z in
                                              range(grid_ranges["Z"][0], grid_ranges["Z"][1] + 1)}
        self.grid[grid_ranges["A"][1] + 1] = {z: [line.copy() for line in blank_xy_grid] for z in
                                              range(grid_ranges["Z"][0], grid_ranges["Z"][1] + 1)}

        for a, xyz_grid in self.grid.items():
            self.grid[a] = {z: xy_grid for z, xy_grid in xyz_grid.items() if
                            grid_ranges["Z"][0] <= z <= grid_ranges["Z"][1]}
            for z, xy_grid in xyz_grid.items():
                self.grid[a][z] = [["."] + x_row[grid_ranges["X"][0]:grid_ranges["X"][1] + 1] + ["."] for x_row in
                                   xy_grid[grid_ranges["Y"][0]:grid_ranges["Y"][1] + 1]]

                self.grid[a][z].insert(0, blank_x_row.copy())
                self.grid[a][z].append(blank_x_row.copy())

                self.grid[a][grid_ranges["Z"][0] - 1] = [line.copy() for line in blank_xy_grid]
                self.grid[a][grid_ranges["Z"][1] + 1] = [line.copy() for line in blank_xy_grid]

    def simulate(self):
        self.correct_grid_size()
        new_grid = {a: {z: [x_row.copy() for x_row in xy_grid] for z, xy_grid in xyz_grid.items()} for a, xyz_grid in
                    self.grid.items()}
        for a_index, xyz_grid in self.grid.items():
            for z_index, xy_grid in xyz_grid.items():
                for y_index, x_row in enumerate(xy_grid):
                    for x_index, cell in enumerate(x_row):
                        active_adjacent = self.get_adjacent_cells(Vector4(x_index, y_index, z_index, a_index)).count(
                            "#")
                        if cell == "#":
                            if not (2 <= active_adjacent <= 3):
                                new_grid[a_index][z_index][y_index][x_index] = "."
                        elif cell == ".":
                            if active_adjacent == 3:
                                new_grid[a_index][z_index][y_index][x_index] = "#"

        self.iteration += 1
        self.grid = new_grid


simulator = Conway_4D(inputlines)
print(simulator)
for sim_index in range(6):
    simulator.simulate()
    if sim_index < 3:
        print(simulator)
    else:
        print(f"Iteration: {sim_index + 1}")

print(f"Number of active cells after 6 cycles: {simulator.get_active_cells()}")
