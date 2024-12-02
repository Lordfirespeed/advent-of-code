from enum import Enum
from common.vectors import Vector2


class Direction(Enum):
    R = Vector2(1, 0)
    U = Vector2(0, 1)
    L = Vector2(-1, 0)
    D = Vector2(0, -1)


def sign(number: int | float) -> int:
    if number == 0:
        return 0
    return 1 if number > 0 else -1


class Solution:
    def __init__(self, movements: [str]) -> None:
        self.movements = movements
        self.head_position = Vector2(0, 0)
        self.tail_position = Vector2(0, 0)
        self.tail_visited_positions = {(0, 0)}

    def move_tail_appropriately(self):
        x_difference = self.head_position.x - self.tail_position.x
        y_difference = self.head_position.y - self.tail_position.y

        if abs(x_difference) <= 1 and abs(y_difference) <= 1:
            return

        delta_vector = Vector2(sign(x_difference), sign(y_difference))
        self.tail_position += delta_vector

    def simulate_step(self, direction: Direction):
        self.head_position += direction.value
        self.move_tail_appropriately()
        self.tail_visited_positions.add(self.tail_position.as_tuple())

    def simulate_movement(self, direction: Direction, quantity: int) -> None:
        for _ in range(quantity):
            self.simulate_step(direction)

    def simulate(self) -> None:
        for movement in self.movements:
            self.simulate_movement(*movement)

    def number_of_positions_tail_visited(self) -> int:
        return len(self.tail_visited_positions)


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        movements = [line.strip().split(" ") for line in input_file.readlines()]
    movements = [(Direction[direction], int(quantity)) for direction, quantity in movements]

    solver = Solution(movements)
    solver.simulate()
    result = solver.number_of_positions_tail_visited()
    print(f"Number of unique positions tail visited: {result}")
