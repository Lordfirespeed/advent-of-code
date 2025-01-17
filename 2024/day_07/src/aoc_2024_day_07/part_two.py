from itertools import product
from typing import Protocol, Sequence

from util.exceptions.no_solution_error import NoSolutionError

from .problem import ProblemInstance, CalibrationEquation


class Operator(Protocol):
    def apply(self, a: int, b: int) -> int: ...


class Add(Operator):
    def apply(self, a: int, b: int) -> int:
        return a + b

    def __repr__(self):
        return "+"


class Multiply(Operator):
    def apply(self, a: int, b: int) -> int:
        return a * b

    def __repr__(self):
        return "*"


class Concatenate(Operator):
    def apply(self, a: int, b: int) -> int:
        return int(str(a) + str(b))

    def __repr__(self):
        return "||"


operators = [
    Add(), Multiply(), Concatenate(),
]

type OperatorAssignment = Sequence[Operator]


def try_operator_assignment(equation: CalibrationEquation, assignment: OperatorAssignment) -> bool:
    assert len(equation.operands) == len(assignment) + 1
    accumulator = equation.operands[0]
    for operator, operand in zip(assignment, equation.operands[1:]):
        accumulator = operator.apply(accumulator, operand)
        if accumulator > equation.result:
            return False
    return accumulator == equation.result


def brute_force_operator_assignment(equation: CalibrationEquation) -> OperatorAssignment:
    operator_count = len(equation.operands) - 1
    for assignment in product(operators, repeat=operator_count):
        assignment_works = try_operator_assignment(equation, assignment)
        if assignment_works:
            return assignment

    raise NoSolutionError


def is_possibly_true(equation: CalibrationEquation) -> bool:
    try:
        brute_force_operator_assignment(equation)
        return True
    except NoSolutionError:
        return False


class PartTwoSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    def solve(self) -> int:
        possibly_true_equations = filter(is_possibly_true, self.instance.equations)
        return sum(equation.result for equation in possibly_true_equations)
