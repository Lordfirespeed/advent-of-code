from __future__ import annotations
from dataclasses import dataclass, field
from typing import Union, Optional
from functools import cached_property


@dataclass
class File:
    name: str
    size: int
    parent: Optional[Directory] = None

    def calculate_size(self, *args, **kwargs):
        return self.size


@dataclass
class Directory:
    name: str
    contents: {str: FileTreeTypes} = field(default_factory=dict)
    parent: Optional[Directory] = None

    def add(self, something: FileTreeTypes) -> None:
        try:
            self.contents[something.name]
            raise KeyError("That filename is in use.")
        except KeyError:
            pass
        self.contents[something.name] = something
        something.parent = self

    def __getitem__(self, name):
        return self.contents[name]

    @cached_property
    def path(self):
        if self.parent is None:
            return self.name
        return self.parent.path + "/" + self.name

    def calculate_size(self, dir_sizes=None):
        if dir_sizes is None:
            dir_sizes = {}

        try:
            return dir_sizes[self.path]
        except KeyError:
            pass

        contents_sizes = []
        for name, something in self.contents.items():
            contents_sizes.append(something.calculate_size(dir_sizes))
        total_size = sum(contents_sizes)
        dir_sizes[self.path] = total_size
        return total_size


FileTreeTypes = Union[File, Directory]


class FileTree:
    def __init__(self):
        self.root = Directory("")

class Solution:
    max_size = 100_000

    def __init__(self, device_stdout: [str]) -> None:
        self.device_stdout: [str] = device_stdout
        self.file_tree = FileTree()
        self.current_working_directory: Directory = None
        self.current_command: str = None
        self.go_to_root()

    def go_to_root(self):
        self.current_working_directory = self.file_tree.root

    def go_up_directory(self):
        self.current_working_directory = self.current_working_directory.parent

    def process_command(self, command: str) -> None:
        self.current_command = command
        if command.startswith("ls"):
            return

        if command.startswith("cd"):
            operand = command[3:]
            self.process_cd_command(operand)
            return

        raise NotImplementedError

    def process_cd_command(self, operand: str) -> None:
        if operand == "/":
            self.go_to_root()
            return

        if operand == "..":
            self.go_up_directory()
            return

        self.current_working_directory = self.current_working_directory[operand]
        assert isinstance(self.current_working_directory, Directory)

    def process_output(self, output: str) -> None:
        if self.current_command.startswith("ls"):
            self.process_ls_output(output)
            return

        raise NotImplementedError

    def process_ls_output(self, output: str) -> None:
        if output.startswith("dir"):
            directory_name = output[4:]
            self.current_working_directory.add(Directory(directory_name))
            return

        size, filename = output.split(" ")
        size = int(size)
        self.current_working_directory.add(File(filename, size))

    def process_device_stdout(self) -> None:
        for stdout in self.device_stdout:
            if stdout.startswith("$ "):
                self.process_command(stdout[2:])
                continue

            self.process_output(stdout)

    def sum_of_small_directories_sizes(self) -> int:
        dir_sizes = {}
        self.file_tree.root.calculate_size(dir_sizes)
        small_sizes = [dir_size for dir_name, dir_size in dir_sizes.items() if dir_size < self.max_size]
        return sum(small_sizes)


if __name__ == "__main__":
    with open(r"input.txt") as input_file:
        device_stdout = [line.strip() for line in input_file.readlines()]

    solver = Solution(device_stdout)
    solver.process_device_stdout()
    result = solver.sum_of_small_directories_sizes()
    print(f"Sum of small directories' sizes: {result}")
