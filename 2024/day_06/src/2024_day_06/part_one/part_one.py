from util.vectors import pos

from ..problem import ProblemInstance

from .guard import Guard


class PartOneSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance
        self.guard = Guard(
            room_obstructions=self.instance.obstructions,
            room_shape=self.instance.initial_room_map.shape,
            location=self.instance.initial_guard_position,
        )

    def solve(self) -> int:
        guard_visited: set[pos] = {self.guard.location}
        guard_visited.update(self.guard.positions())
        return len(guard_visited)
