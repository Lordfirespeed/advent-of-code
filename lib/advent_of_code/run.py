from pathlib import Path
import sys

import aiohttp

from config import config
from problem_instance_abc import ProblemInstanceABC

from .api import advent_of_code_session, fetch_problem_input
from .args import AdventOfCodeArgNamespace
from .scrape import get_problem_title


async def load_problem_instance(args: AdventOfCodeArgNamespace, session: aiohttp.ClientSession) -> ProblemInstanceABC:
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


async def run(args: AdventOfCodeArgNamespace) -> None:
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
