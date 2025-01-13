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

    def antinode_positions(self) -> set[pos]:
        positions = set()
        for first_antenna, second_antenna in combinations(self.antennas, 2):
            position_delta = second_antenna.position - first_antenna.position
            positions.add(first_antenna.position - position_delta)
            positions.add(second_antenna.position + position_delta)
        return positions


class PartOneSolver:
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
            group.add(Antenna(character, map_pos))
        self._antenna_groups = {frequency: AntennaGroup(frozenset(antennas)) for frequency, antennas in mutable_groups.items()}
        
    def is_in_bounds(self, position: pos) -> bool:
        return position in pos_range(self.instance.antenna_map.shape)

    def solve(self) -> int:
        self.discover_antennas()
        antinode_positions: set[pos] = set()
        for group in self.antenna_groups.values():
            antinode_positions |= group.antinode_positions()
        
        out_of_bounds = set(position for position in antinode_positions if not self.is_in_bounds(position))
        antinode_positions.difference_update(out_of_bounds)

        return len(antinode_positions)
        
