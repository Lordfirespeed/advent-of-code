class Solution:
    target_length = 14

    def __init__(self, datastream: str) -> None:
        self.datastream = datastream

    def index_of_first_message(self) -> int:
        """'Sliding window' solution - each step, slide the end of the window forward. if an 'offending' value is found,
            the start of the window slides forwards such that the value is no longer a problem (in this case, such that
            the matching character is removed from the start of the window)"""

        window_start = 0
        window_end = 0
        window = ""

        while window_start < len(self.datastream) - self.target_length:
            new_character = self.datastream[window_end]

            try:
                index_in_window = window.index(new_character)
                window_start += index_in_window + 1
            except ValueError:
                pass

            window_end += 1
            window = self.datastream[window_start:window_end]

            if window_end - window_start == self.target_length:
                return window_end


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        datastream = input_file.readline()

    solver = Solution(datastream)
    result = solver.index_of_first_message()
    print(f"First message marker found after {result} processed characters.")
