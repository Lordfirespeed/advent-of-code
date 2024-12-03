import asyncio

from .args import parser, run_parser, test_parser, AdventOfCodeArgNamespace
from .run import run
from .test import test

parser.set_defaults(main=run, rest_args=[])
run_parser.set_defaults(main=run, rest_args=[])
test_parser.set_defaults(main=test)


async def main() -> None:
    args = parser.parse_args(None, AdventOfCodeArgNamespace())
    await args.main(args)


if __name__ == "__main__":
    asyncio.run(main())
