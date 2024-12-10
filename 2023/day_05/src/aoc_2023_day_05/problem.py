import re
from dataclasses import dataclass
from operator import indexOf
from typing import ClassVar, Self

from problem_instance_abc import ProblemInstanceABC
from util.span import span

@dataclass(frozen=True)
class Item:
    item_id: int
    item_type: str

@dataclass(frozen=True)
class ItemRange:
    item_type: str
    id_ranges: tuple[span, ...]

@dataclass(frozen=True)
class MapRange:
    destination_range_start: int
    source_range_start: int
    length: int

    @property
    def source_range(self) -> span:
        return span(self.source_range_start, self.source_range_start+self.length)

    @property
    def destination_range(self) -> span:
        return span(self.destination_range_start, self.destination_range_start+self.length)

    def __contains__(self, item) -> bool:
        return item in self.source_range

    def __getitem__(self, item) -> int:
        index = self.source_range.index(item)
        return self.destination_range[index]

    @classmethod
    def from_string(cls, map_range_string: str) -> Self:
        map_range_value_strings = map_range_string.split()
        if len(map_range_value_strings) != 3:
            raise ValueError
        destination_range_start_string, source_range_start_string, length_string = map_range_value_strings
        return cls(
            destination_range_start=int(destination_range_start_string),
            source_range_start=int(source_range_start_string),
            length=int(length_string),
        )


@dataclass(frozen=True)
class Map:
    header_line_pattern: ClassVar[re.Pattern] = re.compile(r"^(?P<from_category>\w+?)-to-(?P<to_category>\w+?) map:$")

    from_category: str
    to_category: str
    ranges: list[MapRange]

    def __contains__(self, item) -> bool:
        return any(item in map_range for map_range in self.ranges)

    def __getitem__(self, item) -> int:
        map_range_index = indexOf((item in map_range for map_range in self.ranges), True)
        map_range = self.ranges[map_range_index]
        return map_range[item]

    @classmethod
    def from_string(cls, map_string: str) -> Self:
        lines = map_string.splitlines()
        header_line = lines.pop(0)
        header_line_match = cls.header_line_pattern.match(header_line)
        if header_line_match is None:
            raise ValueError
        ranges = [MapRange.from_string(line) for line in lines]
        return cls(
            from_category=header_line_match.group("from_category"),
            to_category=header_line_match.group("to_category"),
            ranges=ranges,
        )


class ProblemInstance(ProblemInstanceABC):
    seeds: list[Item]
    seed_ranges: list[ItemRange]
    maps: list[Map]

    def parse_seeds(self, seeds_paragraph: str) -> None:
        assert seeds_paragraph.startswith("seeds: ")
        seed_id_strings = seeds_paragraph[7:].split()
        seed_ids = [int(seed_id_string) for seed_id_string in seed_id_strings]
        self.seeds = [Item(seed_id, "seed") for seed_id in seed_ids]

        # https://stackoverflow.com/a/23286299/11045433
        seed_ids_iter = iter(seed_ids)
        self.seed_ranges = [ItemRange("seed", (span(start, start+length),)) for start, length in zip(seed_ids_iter, seed_ids_iter)]

    def parse_maps(self, map_paragraphs: list[str]) -> None:
        self.maps = [Map.from_string(map_paragraph) for map_paragraph in map_paragraphs]

    def parse_plaintext(self) -> None:
        paragraphs = self.input_plaintext.split("\n\n")
        seeds_paragraph = paragraphs.pop(0)
        self.parse_seeds(seeds_paragraph)
        self.parse_maps(paragraphs)
