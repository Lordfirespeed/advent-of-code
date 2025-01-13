from dataclasses import dataclass
from itertools import combinations

from util.exceptions.not_initialised_error import NotInitialisedError
from util.vectors import pos, pos_range

from .problem import ProblemInstance


@dataclass(frozen=True)
class Antenna:
    frequency: str
    position: pos


@dataclass(frozen=True)
class AntennaGroup:
    antennas: frozenset[Antenna]

    def antinode_positions(self, bounds: pos_range) -> set[pos]:
        positions: set[pos] = set()
        for first_antenna, second_antenna in combinations(self.antennas, 2):
            position_delta = second_antenna.position - first_antenna.position
            cursor = first_antenna.position.as_mutable()
            while True:
                positions.add(cursor.as_immutable())
                cursor -= position_delta
                if cursor not in bounds:
                    break
            
            cursor = second_antenna.position.as_mutable()
            while True:
                positions.add(cursor.as_immutable())
                cursor += position_delta
                if cursor not in bounds:
                    break
        return positions


class PartTwoSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance
        self._antenna_groups: dict[str, AntennaGroup] | None = None

    @property
    def antenna_groups(self) -> dict[str, AntennaGroup]:
        if self._antenna_groups is not None:
            return self._antenna_groups
        raise NotInitialisedError

    def discover_antennas(self) -> None:
        mutable_groups: dict[str, set[Antenna]] = {}
        for map_pos in pos_range(self.instance.antenna_map.shape):
            character = self.instance.antenna_map[map_pos]
            if character == ".":
                continue
            group = mutable_groups.get(character, None)
            if group is None:
                group = set()
                mutable_groups[character] = group
            group.add(Antenna(character, map_pos.as_immutable()))
        self._antenna_groups = {frequency: AntennaGroup(frozenset(antennas)) for frequency, antennas in mutable_groups.items()}

    def solve(self) -> int:
        self.discover_antennas()
        antinode_positions: set[pos] = set()
        map_bounds = pos_range(self.instance.antenna_map.shape)
        for group in self.antenna_groups.values():
            antinode_positions |= group.antinode_positions(map_bounds)

        return len(antinode_positions)

