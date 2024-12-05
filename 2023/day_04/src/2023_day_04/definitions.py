from pathlib import Path

problem_source_dir = Path(__file__).resolve().parent.parent  # <repo>/year/day/src
problem_dir = problem_source_dir.parent  # <repo>/year/day
problem_test_instances_dir = Path(problem_dir, "test_instances")
