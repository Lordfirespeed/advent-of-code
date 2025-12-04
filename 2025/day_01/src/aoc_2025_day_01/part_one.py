from .problem import ProblemInstance, Turn, TurnDirection


class PartOneSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance
        self.dial_position = 50
        self.zero_count = 0

    def do_turn(self, turn: Turn) -> None:
        sign = +1 if turn.direction is TurnDirection.Right else -1
        self.dial_position = (self.dial_position + sign * turn.distance) % 100
        if self.dial_position == 0: self.zero_count += 1

    def solve(self) -> int:
        for turn in self.instance.turns:
            self.do_turn(turn)

        return self.zero_count
