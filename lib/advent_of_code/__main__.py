import argparse
import asyncio
import importlib
from pathlib import Path
import sys
from typing import Awaitable, Callable, Self, Type

import aiohttp
from bs4 import BeautifulSoup

from advent_of_code.api import advent_of_code_session, fetch_problem_input, fetch_problem_html
from advent_of_code.scrape_problem_title import scrape_problem_title
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


async def load_problem_instance(args: ProblemSolverArgNamespace, session: aiohttp.ClientSession) -> ProblemInstanceABC:
    instance_cache_path = Path(args.problem_dir, "cache", "input.txt")
    if instance_cache_path.exists():
        print("Using cached problem input")
        return args.instance_type.from_file(instance_cache_path)

    print("Fetching problem input")
    instance_plaintext = await fetch_problem_input(session, args.problem_year, args.problem_day)
    instance_cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(instance_cache_path, "w") as instance_cache_handle:
        instance_cache_handle.write(instance_plaintext)
    print("Fetched & cached problem input")
    return args.instance_type(instance_plaintext)


async def get_problem_html_soup(args: ProblemSolverArgNamespace, session: aiohttp.ClientSession) -> BeautifulSoup:
    html_cache_path = Path(args.problem_dir, "cache", "problem.html")
    if html_cache_path.exists():
        with open(html_cache_path) as html_cache_handle:
            return BeautifulSoup(html_cache_handle, features="html.parser")

    problem_html = await fetch_problem_html(session, args.problem_year, args.problem_day)
    html_cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(html_cache_path, "w") as html_cache_handle:
        html_cache_handle.write(problem_html)
        html_cache_handle.write("\n")
    return BeautifulSoup(problem_html, features="html.parser")


async def get_problem_title(args: ProblemSolverArgNamespace, session: aiohttp.ClientSession) -> str:
    title_cache_path = Path(args.problem_dir, "cache", "title.txt")
    if title_cache_path.exists():
        with open(title_cache_path) as title_cache_handle:
            return title_cache_handle.readline().strip()

    soup = await get_problem_html_soup(args, session)
    title = scrape_problem_title(soup)
    title_cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(title_cache_path, "w") as title_cache_handle:
        title_cache_handle.write(title)
        title_cache_handle.write("\n")
    return title


async def run(args: ProblemSolverArgNamespace) -> None:
    sys.path.append(str(Path(args.problem_dir, "src")))

    advent_of_code_session_token = config.get("ADVENT_OF_CODE_SESSION", None)
    assert advent_of_code_session_token is not None
    async with advent_of_code_session(advent_of_code_session_token) as session:
        title = await get_problem_title(args, session)
        print(f"--- {args.problem_year} Day {args.problem_day}: {title} ---")
        instance = await load_problem_instance(args, session)

    part_one_solver = args.part_one_solver_factory(instance)
    part_one_solution = part_one_solver.solve()
    print(f"Part one: {part_one_solution}")

    part_two_solver = args.part_two_solver_factory(instance)
    part_two_solution = part_two_solver.solve()
    print(f"Part two: {part_two_solution}")


async def test(args: ProblemSolverArgNamespace) -> None:
    sys.path.append(str(Path(args.problem_dir, "src")))
    import unittest
    unittest.main(module=f"{args.solver_module_name}.test", argv=["unittest", *args.rest_args])


parser.set_defaults(main=run, rest_args=[])
run_parser.set_defaults(main=run, rest_args=[])
test_parser.set_defaults(main=test)


async def main() -> None:
    args = parser.parse_args(None, ProblemSolverArgNamespace())
    await args.main(args)


if __name__ == "__main__":
    asyncio.run(main())
