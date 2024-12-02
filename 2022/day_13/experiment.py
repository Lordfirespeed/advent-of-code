from part_one import PacketParser, Solution

with open("expected_test_output.txt") as expected_output_file:
    packets = [PacketParser.parse_string(line) for line in expected_output_file]

solver = Solution([])
