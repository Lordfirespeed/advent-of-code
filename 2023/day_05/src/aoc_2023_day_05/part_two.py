from functools import reduce
from typing import Iterable

from util.span import span

from .problem import ProblemInstance, Map, Item, ItemRange


class PartTwoSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    @classmethod
    def apply(cls, item_map: Map, item_range: ItemRange) -> ItemRange:
        if item_range.item_type != item_map.from_category:
            raise ValueError(f"Can't apply {item_map} to {item_range}")
        from_id_spans = list(item_range.id_ranges)
        to_id_spans = []
        
        for map_range in item_map.ranges:
            for from_id_span_index in reversed(range(len(from_id_spans))):
                from_id_span = from_id_spans[from_id_span_index]
                intersection = from_id_span.intersection(map_range.source_range)
                if len(intersection) == 0:
                    continue

                mapped_range = map_range.destination_range[map_range.source_range.index(intersection)]
                to_id_spans.append(mapped_range)
                
                diff_left, diff_right = from_id_span.difference(map_range.source_range)
                if len(diff_left) > 0 and len(diff_right) > 0:
                    from_id_spans[from_id_span_index:from_id_span_index+1] = (diff_left, diff_right)
                elif len(diff_left) > 0:
                    from_id_spans[from_id_span_index] = diff_left
                elif len(diff_right) > 0:
                    from_id_spans[from_id_span_index] = diff_right
                else:
                    from_id_spans.pop(from_id_span_index)

        return ItemRange(item_map.to_category, (*from_id_spans, *to_id_spans))

    def apply_all(self, item_range: ItemRange) -> ItemRange:
        return reduce(lambda item_range, item_map: self.apply(item_map, item_range), self.instance.maps, item_range)

    def location_range_for(self, item: ItemRange) -> tuple[span, ...]:
        assert item.item_type == "seed"
        mapped_item = self.apply_all(item)
        assert mapped_item.item_type == "location"
        return mapped_item.id_ranges

    def location_ranges_for_seeds(self) -> Iterable[span]:
        for seed in self.instance.seed_ranges:
            yield from self.location_range_for(seed)
    
    def min_locations_for_seeds(self) -> Iterable[int]:
        for location_id_range in self.location_ranges_for_seeds():
            yield location_id_range.start

    def solve(self) -> int:
        return min(self.min_locations_for_seeds())
