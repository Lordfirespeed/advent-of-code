from problem_instance_abc import ProblemInstanceABC


class ProblemInstance(ProblemInstanceABC):
    memory: str

    def parse_plaintext(self) -> None:
        self.memory = "".join(self.input_plaintext.splitlines())
