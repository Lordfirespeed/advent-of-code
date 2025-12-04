import asyncio

from .args import parser, run_parser, test_parser, AdventOfCodeArgNamespace, init_parser
from .init_problem import init_problem
from .run import run
from .test import test

parser.set_defaults(main=run, rest_args=[])
init_parser.set_defaults(main=init_problem)
run_parser.set_defaults(main=run)
test_parser.set_defaults(main=test)


async def main() -> None:
    args = parser.parse_args(None, AdventOfCodeArgNamespace())
    await args.main(args)


if __name__ == "__main__":
    asyncio.run(main())
