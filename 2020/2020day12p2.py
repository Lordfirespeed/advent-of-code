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

    def __sub__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x - other.x, self.y - other.y)
        elif type(other) == int:
            return Vector2(self.x - other, self.y - other)

    def __mul__(self, other):
        if type(other) == Vector2:
            return self.x * other.x + self.y * other.y
        elif type(other) == int:
            return Vector2(self.x * other, self.y * other)

    def rotate_about_acw(self, other, times: int):
        times %= 4
        relative_position = Vector2(self.x - other.x, self.y - other.y)
        for t in range(times):
            relative_position = Vector2(-relative_position.y, relative_position.x)
        return other + relative_position

    def rotate_about_cw(self, other, times: int):
        times %= 4
        relative_position = Vector2(self.x - other.x, self.y - other.y)
        for t in range(times):
            relative_position = Vector2(relative_position.y, -relative_position.x)
        return other + relative_position

    def __repr__(self):
        return f"({self.x}, {self.y})"


waypoint = Vector2(10, 1)
position = Vector2(0, 0)
facing = "E"
direction_map = {"N": Vector2(0, 1), "E": Vector2(1, 0), "S": Vector2(0, -1), "W": Vector2(-1, 0)}
directions = "NESW"

for move in moves:
    if move[0] in "NESW":
        waypoint += direction_map[move[0]] * int(move[1:])
    elif move[0] in "LR":
        turntimes = int(move[1:]) // 90
        if move[0] == "R":
            waypoint = waypoint.rotate_about_cw(Vector2(0, 0), turntimes)
        elif move[0] == "L":
            waypoint = waypoint.rotate_about_acw(Vector2(0, 0), turntimes)
    elif move[0] == "F":
        position += waypoint * int(move[1:])

print(f"Manhattan distance from starting position: {abs(position)}")
