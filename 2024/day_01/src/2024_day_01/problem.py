from problem_instance_abc import ProblemInstanceABC


class ProblemInstance(ProblemInstanceABC):
    left_list: tuple[int, ...]
    right_list: tuple[int, ...]

    def parse_plaintext(self) -> None:
        lines = self.input_plaintext.splitlines()
        left_list: list[int] = []
        right_list: list[int] = []
        for line in lines:
            left_value, right_value = line.split()
            left_list.append(int(left_value))
            right_list.append(int(right_value))

        self.left_list = tuple(left_list)
        self.right_list = tuple(right_list)
