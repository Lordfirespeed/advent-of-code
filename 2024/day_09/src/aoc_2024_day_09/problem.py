from problem_instance_abc import ProblemInstanceABC


class ProblemInstance(ProblemInstanceABC):
    disk_map: str

    def parse_plaintext(self) -> None:
        lines = self.input_plaintext.splitlines()
        self.disk_map = lines.pop()
        assert len(lines) == 0
