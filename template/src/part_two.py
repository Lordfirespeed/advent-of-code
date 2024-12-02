class Solution:
    def __init__(self, input_lines: [str]) -> None:
        self.input_lines = input_lines

    def foo(self) -> int:
        return len(self.input_lines)


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        input_lines = [line.strip() for line in input_file.readlines()]

    solver = Solution(input_lines)
    result = solver.foo()
    print(f"foo: {result}")
