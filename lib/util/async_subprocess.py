import asyncio
from dataclasses import dataclass
import os
from pathlib import Path


@dataclass
class SubprocessResult:
    exit_code: int
    stdout: str
    stderr: str


async def run(
    cmd: str,
    env: dict[str, str] | None = None,
    cwd: Path | None = None,
) -> SubprocessResult:
    if env is None:
        env = os.environ.copy()

    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env,
        cwd=cwd,
    )
    stdout, stderr = await proc.communicate()

    if (code := proc.returncode) is None:
        code = 1

    return SubprocessResult(
        code,
        stdout.decode("utf8", errors="ignore").rstrip(),
        stderr.decode("utf8", errors="ignore").rstrip(),
    )


__all__ = ("run", "SubprocessResult")
