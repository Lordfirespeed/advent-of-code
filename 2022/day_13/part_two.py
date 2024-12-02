from part_one import PacketParser, OrderState, Solution, Payload
from math import prod as product


class PartTwoSolution(Solution):
    divider_payloads = [
        [[2]],
        [[6]]
    ]

    def __init__(self, packet_strings: [str]) -> None:
        self.packets = [PacketParser.parse_string(packet_string) for packet_string in packet_strings]
        self.packets = self.divider_payloads + self.packets

    def sort(self):
        self.packets = self.sort_packets(self.packets)

    @classmethod
    def partition(cls, packets: [Payload], pivot: Payload) -> tuple[list[Payload], list[Payload], list[Payload]]:
        left, centre, right = [], [], []

        for compare_packet in packets:
            order_state = cls.compare(pivot, compare_packet)
            if order_state == OrderState.CorrectOrder:
                right.append(compare_packet)
                continue

            if order_state == OrderState.Neither:
                centre.append(compare_packet)
                continue

            if order_state == OrderState.WrongOrder:
                left.append(compare_packet)
                continue

            raise NotImplementedError

        return left, centre, right

    @classmethod
    def sort_packets(cls, packets: [Payload]) -> [Payload]:
        if len(packets) <= 1:
            return packets

        pivot = packets[0]
        left, centre, right = cls.partition(packets[1:], pivot)
        centre.append(pivot)

        sorted_left = cls.sort_packets(left)
        sorted_right = cls.sort_packets(right)

        return sorted_left + centre + sorted_right

    def decoder_key(self):
        divider_indexes = [self.packets.index(divider) + 1 for divider in self.divider_payloads]
        return product(divider_indexes)


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        packets_strings = [line.strip() for line in input_file.readlines()]
    packets_strings = filter("".__ne__, packets_strings)

    solver = PartTwoSolution(packets_strings)
    solver.sort()
    result = solver.decoder_key()
    print(f"Distress signal decoder key: {result}")
