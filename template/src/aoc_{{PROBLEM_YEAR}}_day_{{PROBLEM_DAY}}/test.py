import unittest
from pathlib import Path

from .definitions import problem_test_instances_dir
from .part_one import PartOneSolver
from .part_two import PartTwoSolver
from .problem import ProblemInstance


def load_instance(instance_name: str) -> ProblemInstance:
    return ProblemInstance.from_file(Path(problem_test_instances_dir, instance_name))


class TestPartOne(unittest.TestCase):
    def test_example_01(self):
        instance = load_instance("example-01.txt")
        solver = PartOneSolver(instance)
        self.assertEqual(7, solver.solve())


class TestPartTwo(unittest.TestCase):
    def test_example_01(self):
        instance = load_instance("example-01.txt")
        solver = PartTwoSolver(instance)
        self.assertEqual(7, solver.solve())


if __name__ == "__main__":
    unittest.main()
