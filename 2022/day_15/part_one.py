from common.vectors import Vector2
from common.spans import Span, SpanCollection
import re
from dataclasses import dataclass, field
from typing import ClassVar, Self


@dataclass
class Sensor:
    position: Vector2 = field(compare=True)
    closest_beacon_position: Vector2 = field(compare=False)

    @property
    def radius(self) -> int:
        return (self.closest_beacon_position - self.position).manhattan

    @property
    def diameter(self) -> int:
        return self.radius * 2 + 1

    sensor_data_pattern: ClassVar[re.Pattern] = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

    @classmethod
    def from_data(cls, sensor_data: str) -> Self:
        match = re.match(cls.sensor_data_pattern, sensor_data)
        assert match is not None
        groups = match.groups()
        position = Vector2(int(groups[0]), int(groups[1]))
        closest_beacon_position = Vector2(int(groups[2]), int(groups[3]))
        return cls(position, closest_beacon_position)

    def span_at_y(self, y: int) -> Span:
        y_difference = abs(self.position.y - y)
        if y_difference > self.radius:
            raise ValueError("Sensor has no span at provided y value")
        span_radius = (self.radius - y_difference)
        return Span(self.position.x - span_radius, self.position.x + span_radius + 1)


class Solution:
    considering_y_coordinate = 2000000

    def __init__(self, sensor_datas: [str]) -> None:
        self.sensors = [Sensor.from_data(sensor_data) for sensor_data in sensor_datas]
        self.beacon_positions = set([sensor.closest_beacon_position for sensor in self.sensors])

    def beacon_positions_on_row(self) -> [int]:
        return [position.x for position in filter(lambda position: position.y == self.considering_y_coordinate, self.beacon_positions)]

    def positions_spanned_on_row(self) -> SpanCollection:
        unsimplified_spans = []
        for sensor in self.sensors:
            try:
                unsimplified_spans.append(sensor.span_at_y(self.considering_y_coordinate))
            except ValueError:
                pass

        return SpanCollection(*unsimplified_spans)

    def positions_with_no_beacon_on_row(self) -> [int]:
        spans = self.positions_spanned_on_row()
        beacon_positions = self.beacon_positions_on_row()

        beacons_in_span = [position in spans for position in beacon_positions].count(True)

        return sum([span.stop - span.start for span in spans._spans]) - beacons_in_span


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        sensor_datas = [line.strip() for line in input_file.readlines()]

    solver = Solution(sensor_datas)
    result = solver.positions_with_no_beacon_on_row()
    print(f"Positions that cannot contain a beacon in row at y={solver.considering_y_coordinate}: {result}")
