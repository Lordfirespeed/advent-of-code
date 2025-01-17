from problem_instance_abc import ProblemInstanceABC


class ProblemInstance(ProblemInstanceABC):
    document: list[str]

    def parse_plaintext(self) -> None:
        self.document = self.input_plaintext.splitlines()
