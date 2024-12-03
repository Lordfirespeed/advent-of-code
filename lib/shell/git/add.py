from logging import Logger, getLogger
from pathlib import Path

from util import async_subprocess

from ._set_env import set_env


async def add(repository: Path, add_paths: list[Path], logger: Logger | None = None) -> None:
    logger = logger if logger is not None else getLogger(__name__)
    
    add_path_args = " ".join(f"'{add_path}'" for add_path in add_paths)

    result = await async_subprocess.run(
        f"git -C '{repository}' add {add_path_args}",
        set_env(),
    )

    if result.exit_code == 0:
        return

    raise Exception(f"`git add {add_path_args}` exited with status {result.exit_code}; {result.stderr}")
