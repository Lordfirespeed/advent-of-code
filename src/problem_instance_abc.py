from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Self


@dataclass
class ProblemInstanceABC(ABC):
    input_plaintext: str

    @abstractmethod
    def parse_plaintext(self) -> None: ...

    def __post_init__(self):
        self.parse_plaintext()

    @classmethod
    def from_file(cls, file_path: Path) -> Self:
        with open(file_path, "r") as file_handle:
            plaintext = file_handle.read()
        return cls(plaintext)
