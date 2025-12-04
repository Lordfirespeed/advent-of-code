from util.span import span

from problem_instance_abc import ProblemInstanceABC



class ProblemInstance(ProblemInstanceABC):
    ranges: list[span]

    @staticmethod
    def parse_raw_range(raw_range: str) -> span:
        lower_bound_str, upper_bound_str = raw_range.split("-")
        lower_bound = int(lower_bound_str)
        upper_bound = int(upper_bound_str)
        return span(lower_bound, upper_bound+1)

    def parse_plaintext(self) -> None:
        lines = self.input_plaintext.splitlines()
        delimited_raw_ranges = "".join(lines)
        raw_ranges = delimited_raw_ranges.split(",")
        self.ranges = [self.parse_raw_range(raw_range) for raw_range in raw_ranges]

