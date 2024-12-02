from problem_instance_abc import ProblemInstanceABC


class ProblemInstance(ProblemInstanceABC):
    reports: list[list[int]]

    def parse_plaintext(self) -> None:
        report_strings = self.input_plaintext.splitlines()
        self.reports = [[int(level) for level in report_string.split()] for report_string in report_strings]
