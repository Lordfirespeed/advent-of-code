from functools import reduce
from typing import Iterable

from .problem import ProblemInstance, Map, Item


class PartOneSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    @classmethod
    def apply(cls, item_map: Map, item: Item) -> Item:
        if item.item_type != item_map.from_category:
            raise ValueError(f"Can't apply {item_map} to {item}")
        new_item_id = item.item_id
        if item.item_id in item_map:
            new_item_id = item_map[item.item_id]
        return Item(new_item_id, item_map.to_category)

    def apply_all(self, item: Item) -> Item:
        return reduce(lambda item, item_map: self.apply(item_map, item), self.instance.maps, item)

    def location_for(self, item: Item) -> int:
        assert item.item_type == "seed"
        mapped_item = self.apply_all(item)
        assert mapped_item.item_type == "location"
        return mapped_item.item_id

    def locations_for_seeds(self) -> Iterable[int]:
        for seed in self.instance.seeds:
            yield self.location_for(seed)

    def solve(self) -> int:
        return min(self.locations_for_seeds())
