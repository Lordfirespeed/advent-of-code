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
    number_of_knots = 10

    def __init__(self, movements: [str]) -> None:
        self.movements = movements
        self.knot_positions = [Vector2(0, 0) for _ in range(self.number_of_knots)]
        self.tail_visited_positions = {(0, 0)}

    @staticmethod
    def move_knot_appropriately(knot_to_move: Vector2, knot_in_front: Vector2) -> None:
        x_difference = knot_in_front.x - knot_to_move.x
        y_difference = knot_in_front.y - knot_to_move.y

        if abs(x_difference) <= 1 and abs(y_difference) <= 1:
            return

        delta_vector = Vector2(sign(x_difference), sign(y_difference))
        knot_to_move += delta_vector

    def simulate_step(self, direction: Direction):
        self.knot_positions[0] += direction.value
        for knot_to_move, knot_in_front in zip(self.knot_positions[1:], self.knot_positions[:-1]):
            self.move_knot_appropriately(knot_to_move, knot_in_front)
        self.tail_visited_positions.add(self.knot_positions[-1].as_tuple())

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
