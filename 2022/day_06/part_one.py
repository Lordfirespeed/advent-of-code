class Solution:
    target_length = 4
    def __init__(self, datastream: str) -> None:
        self.datastream = datastream

    def index_of_first_marker(self) -> int:
        """The 'naive' solution - will not work for large target_length"""
        for current_index in range(len(self.datastream) - self.target_length):
            datastream_slice = datastream[current_index:current_index + self.target_length]
            if len(set(datastream_slice)) == self.target_length:
                return current_index + self.target_length


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        datastream = input_file.readline()

    solver = Solution(datastream)
    result = solver.index_of_first_marker()
    print(f"First packet marker found after {result} processed characters.")
