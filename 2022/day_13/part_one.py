from typing import TypeVar, Self
from json import loads as json_load_string
from enum import Enum, auto

Payload = TypeVar("Payload", int, list[int | Self])


class PacketParser:
    @staticmethod
    def parse_string(packet_string: str) -> Payload:
        payload = json_load_string(packet_string)
        return payload


class OrderState(Enum):
    CorrectOrder = auto()
    WrongOrder = auto()
    Neither = auto()


class Solution:
    def __init__(self, packet_pair_strings: [str]) -> None:
        self.packet_pair_strings = packet_pair_strings
        self.correct_order_indexes = []

    @classmethod
    def compare(cls, left: Payload, right: Payload) -> OrderState:
        if isinstance(left, int) and isinstance(right, list):
            return cls.compare([left], right)

        if isinstance(left, list) and isinstance(right, int):
            return cls.compare(left, [right])

        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return OrderState.CorrectOrder

            if left > right:
                return OrderState.WrongOrder

            return OrderState.Neither

        if isinstance(left, list) and isinstance(right, list):
            comparing_index = 0
            while comparing_index < len(left) and comparing_index < len(right):
                order_state = cls.compare(left[comparing_index], right[comparing_index])
                if order_state != OrderState.Neither:
                    return order_state
                comparing_index += 1

            if len(left) == comparing_index == len(right):
                return OrderState.Neither

            if comparing_index == len(left):
                return OrderState.CorrectOrder

            if comparing_index == len(right):
                return OrderState.WrongOrder

        raise TypeError

    @classmethod
    def compare_pair_string(cls, packet_pair_string: str) -> OrderState:
        left_string, right_string = packet_pair_string.split("\n")
        left_payload, right_payload = PacketParser.parse_string(left_string), PacketParser.parse_string(right_string)
        return cls.compare(left_payload, right_payload)

    def make_comparisons(self) -> None:
        for pair_index, packet_pair_string in enumerate(self.packet_pair_strings, 1):
            order_state = self.compare_pair_string(packet_pair_string)

            if order_state == OrderState.Neither:
                print("Something definitely went wrong")

            if order_state != OrderState.CorrectOrder:
                continue

            self.correct_order_indexes.append(pair_index)

    def correct_order_index_sum(self) -> int:
        return sum(self.correct_order_indexes)


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        packets_string = input_file.read()
    packet_pair_strings = packets_string.split("\n\n")

    solver = Solution(packet_pair_strings)
    solver.make_comparisons()
    result = solver.correct_order_index_sum()
    print(f"Correct order packet pair index sum: {result}")
