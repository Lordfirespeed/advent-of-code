from pathlib import Path
from typing import TypedDict

from config import config
from definitions import project_root_dir
from shell import git
from skeleton_builder.generate import use_template

from .api import advent_of_code_session
from .args import AdventOfCodeArgNamespace
from .scrape import get_problem_title

problem_template_dir = Path(project_root_dir, "template")


class ProblemTemplateContext(TypedDict):
    PROBLEM_YEAR: str
    PROBLEM_DAY: str


async def init_problem(args: AdventOfCodeArgNamespace) -> None:
    context: ProblemTemplateContext = {
        "PROBLEM_YEAR": f"{args.problem_year:04}",
        "PROBLEM_DAY": f"{args.problem_day:02}",
    }

    if not args.problem_dir.exists():
        use_template(args.problem_dir, problem_template_dir, context)
        await git.add(project_root_dir, [args.problem_dir])

    advent_of_code_session_token = config.get("ADVENT_OF_CODE_SESSION", None)
    assert advent_of_code_session_token is not None
    async with advent_of_code_session(advent_of_code_session_token) as session:
        title = await get_problem_title(args, session)
        print(f"--- {args.problem_year} Day {args.problem_day}: {title} ---")

    print(f"Briefing: https://adventofcode.com/{args.problem_year}/day/{args.problem_day}")
