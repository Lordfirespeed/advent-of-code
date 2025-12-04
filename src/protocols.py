from typing import Protocol

from problem_instance_abc import ProblemInstanceABC


class SupportsSolve(Protocol):
    def solve(self) -> object: ...


class SupportsInstantiateWithProblemInstance[T: ProblemInstanceABC](Protocol):
    def __init__(self, instance: T) -> None: ...


class ProblemSolver[T: ProblemInstanceABC](
    SupportsSolve,
    SupportsInstantiateWithProblemInstance[T]
):
    pass
