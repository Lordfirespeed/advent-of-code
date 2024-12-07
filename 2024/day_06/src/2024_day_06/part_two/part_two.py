from multiprocessing import Pool
from util.vectors import pos, pos_range

from ..problem import ProblemInstance

from .guard import Guard


class PartTwoSolver:

    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    def try_adding_obstacle_at(self, add_obstacle_position: pos) -> bool:
        if add_obstacle_position == self.instance.initial_guard_position:
            return False
        if add_obstacle_position in self.instance.obstructions:
            return False
        
        guard = Guard(
            room_obstructions={add_obstacle_position} | self.instance.obstructions,
            room_shape=self.instance.initial_room_map.shape,
            location=self.instance.initial_guard_position,
        )
        return guard.detect_cycle()

    def solve(self) -> int:
        with Pool(100) as p:
            results = p.map(self.try_adding_obstacle_at, pos_range(self.instance.initial_room_map.shape))
        return results.count(True)
