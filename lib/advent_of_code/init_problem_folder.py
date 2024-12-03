from pathlib import Path
from typing import TypedDict

from definitions import project_root_dir
from skeleton_builder.generate import use_template

from .args import AdventOfCodeArgNamespace


problem_template_dir = Path(project_root_dir, "template")


class ProblemTemplateContext(TypedDict):
    PROBLEM_YEAR: str
    PROBLEM_DAY: str


async def init_problem_folder(args: AdventOfCodeArgNamespace) -> None:
    context: ProblemTemplateContext = { 
        "PROBLEM_YEAR": f"{args.problem_year:04}",
        "PROBLEM_DAY": f"{args.problem_day:02}",
    }
    use_template(args.problem_dir, problem_template_dir, context)
