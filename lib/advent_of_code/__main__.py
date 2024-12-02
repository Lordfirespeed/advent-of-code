import argparse
import asyncio
import importlib
from pathlib import Path
from typing import Awaitable, Callable, Self, Type

from advent_of_code.api import advent_of_code_session, fetch_problem_input
from config import config
from definitions import project_root_dir
from problem_instance_abc import ProblemInstanceABC
from protocols import ProblemSolver


class ProblemSolverArgNamespace(argparse.Namespace):
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


async def run(args: ProblemSolverArgNamespace) -> None:
    instance_cache_path = Path(args.problem_dir, "cache", "input.txt")
    if instance_cache_path.exists():
        instance = args.instance_type.from_file(instance_cache_path)
    else:
        advent_of_code_session_token = config.get("ADVENT_OF_CODE_SESSION", None)
        assert advent_of_code_session_token is not None
        async with advent_of_code_session(advent_of_code_session_token) as session:
            instance_plaintext = await fetch_problem_input(session, args.problem_year, args.problem_day)
        instance_cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(instance_cache_path, "w") as instance_cache_handle:
            instance_cache_handle.write(instance_plaintext)
        instance = args.instance_type(instance_plaintext)

    part_one_solver = args.part_one_solver_factory(instance)
    part_one_solution = part_one_solver.solve()
    print(f"Part one: {part_one_solution}")

    part_two_solver = args.part_two_solver_factory(instance)
    part_two_solution = part_two_solver.solve()
    print(f"Part two: {part_two_solution}")


async def test(args: ProblemSolverArgNamespace) -> None:
    import unittest
    print(args.rest_args)
    unittest.main(module=f"{args.solver_module_name}.test", argv=["unittest", *args.rest_args])


parser.set_defaults(main=run, rest_args=[])
run_parser.set_defaults(main=run, rest_args=[])
test_parser.set_defaults(main=test)


async def main() -> None:
    args = parser.parse_args(None, ProblemSolverArgNamespace())
    await args.main(args)


if __name__ == "__main__":
    asyncio.run(main())
