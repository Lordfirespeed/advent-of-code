import argparse
import importlib
from pathlib import Path
from typing import Awaitable, Callable, Self, Type

from definitions import project_root_dir
from problem_instance_abc import ProblemInstanceABC
from protocols import ProblemSolver


class AdventOfCodeArgNamespace(argparse.Namespace):
    main: Callable[[Self], Awaitable[None]]
    problem_year: int
    problem_day: int
    rest_args: list[str]

    @property
    def solver_module_name(self) -> str:
        return f"{self.problem_year:04}_day_{self.problem_day:02}"

    @property
    def part_one_solver_factory(self) -> Type[ProblemSolver]:
        module = importlib.import_module(f"{self.solver_module_name}.part_one")
        return module.PartOneSolver

    @property
    def part_two_solver_factory(self) -> Type[ProblemSolver]:
        module = importlib.import_module(f"{self.solver_module_name}.part_two")
        return module.PartTwoSolver

    @property
    def problem_dir(self) -> Path:
        return Path(project_root_dir, f"{self.problem_year:04}", f"day_{self.problem_day:02}")

    @property
    def instance_type(self) -> Type[ProblemInstanceABC]:
        module = importlib.import_module(f"{self.solver_module_name}.problem")
        return module.ProblemInstance


parser = argparse.ArgumentParser(
    prog="advent_of_code",
)

parser.add_argument("-y", "--year", required=True, dest="problem_year", metavar="year", type=int)
parser.add_argument("-d", "--day", required=True, dest="problem_day", metavar="day", type=int)

subparsers = parser.add_subparsers(required=False)

run_parser = subparsers.add_parser("run")

test_parser = subparsers.add_parser("test", add_help=False, prefix_chars="+")
test_parser.add_argument("rest_args", nargs=argparse.REMAINDER, metavar="...")