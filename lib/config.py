from pathlib import Path

from dotenv import dotenv_values

from definitions import project_root_dir

config = dotenv_values(Path(project_root_dir, ".env"))
