from common.vectors import Vector2
from common.spans import Span
from common.numeric import Infinity, NegativeInfinity
from part_one import Solution as OldSolution


class Solution(OldSolution):
    considering_y_coordinate = 0
    considering_coordinate_range = range(0, 4_000_001)

    def find_beacon_position(self) -> Vector2:
        for y in self.considering_coordinate_range:
            if y % 10000 == 0:
                print(f"Considering row {y}...")
            self.considering_y_coordinate = y
            spanned = self.positions_spanned_on_row()
            spanned -= Span(NegativeInfinity, self.considering_coordinate_range.start)
            spanned -= Span(self.considering_coordinate_range.stop - 1, Infinity)
            if spanned.has_discontinuities:
                break

        x_coordinate = spanned._spans[0].stop
        return Vector2(x_coordinate, y)

    @staticmethod
    def tuning_frequency(position: Vector2) -> int:
        return position.x * 4_000_000 + position.y


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        sensor_datas = [line.strip() for line in input_file.readlines()]

    solver = Solution(sensor_datas)
    result = solver.find_beacon_position()
    print(f"Position of unknown beacon: {result}")
    print(f"Tuning frequency of that position: {solver.tuning_frequency(result)}")
