with open(r"Input\2020day12.txt") as inputfile:
    moves = [line.strip() for line in inputfile.readlines()]


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __abs__(self):
        return abs(self.x) + abs(self.y)

    def __add__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x + other.x, self.y + other.y)
        elif type(other) == int:
            return Vector2(self.x + other, self.y + other)

    def __mul__(self, other):
        if type(other) == Vector2:
            return self.x * other.x + self.y * other.y
        elif type(other) == int:
            return Vector2(self.x * other, self.y * other)

    def __repr__(self):
        return f"({self.x}, {self.y})"


position = Vector2(0, 0)
facing = "E"
direction_map = {"N": Vector2(0, 1), "E": Vector2(1, 0), "S": Vector2(0, -1), "W": Vector2(-1, 0)}
directions = "NESW"

for move in moves:
    if move[0] in "NESW":
        position += direction_map[move[0]] * int(move[1:])
    elif move[0] in "LR":
        turntimes = int(move[1:]) // 90
        new_dir_index = (directions.index(facing) + {"L": -1, "R": 1}[move[0]] * turntimes) % len(directions)
        facing = directions[new_dir_index]
    elif move[0] == "F":
        position += direction_map[facing] * int(move[1:])

print(f"Manhattan distance from starting position: {abs(position)}")
