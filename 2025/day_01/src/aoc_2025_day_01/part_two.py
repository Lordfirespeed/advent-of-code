from .problem import ProblemInstance, Turn, TurnDirection


class PartTwoSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance
        self.dial_position = 50
        self.zero_count = 0

    def do_turn(self, turn: Turn) -> None:
        sign = +1 if turn.direction is TurnDirection.Right else -1
        old_position = self.dial_position
        self.dial_position += sign * turn.distance
        overflows, new_position = divmod(self.dial_position, 100)
        # if underflow occurs and dial was previously at zero, we didn't visit zero an extra time
        if overflows < 0 and old_position == 0:
            overflows += 1
        self.zero_count += abs(overflows)
        self.dial_position = new_position
        # if no overflow occurs and dial is now pointing at zero, we visited zero an extra time
        if overflows <= 0 and new_position == 0:
            self.zero_count += 1

    def solve(self) -> int:
        for turn in self.instance.turns:
            self.do_turn(turn)

        return self.zero_count
