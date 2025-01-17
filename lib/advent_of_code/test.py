import sys
from pathlib import Path

from .args import AdventOfCodeArgNamespace


async def test(args: AdventOfCodeArgNamespace) -> None:
    sys.path.append(str(Path(args.problem_dir, "src")))
    import unittest
    unittest.main(module=f"{args.solver_module_name}.test", argv=["unittest", *args.rest_args])
