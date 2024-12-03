import contextlib
import os
from pathlib import Path
from typing import Iterator


@contextlib.contextmanager
def work_in(dirname: Path | str | None = None) -> Iterator[None]:
    """Context manager version of os.chdir.

    When exited, returns to the working directory prior to entering.
    """
    current_working_dir = os.getcwd()
    try:
        if dirname is not None:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(current_working_dir)
