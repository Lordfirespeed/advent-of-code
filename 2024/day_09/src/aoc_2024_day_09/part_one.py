from dataclasses import dataclass
from enum import Flag

from util.bit_set import BitSet

from .problem import ProblemInstance


class DiskMapMode(Flag):
    File = 0
    FreeSpace = 1


@dataclass(frozen=True)
class File:
    id: int


class Disk:
    def __init__(self, disk_map: str) -> None:
        self.blocks: list[File | None] = []
        self.block_usage = BitSet()
        self.files: set[File] = set()

        mode: DiskMapMode = DiskMapMode.File
        next_file_id = 0
        for character in disk_map:
            value = int(character)

            if mode is DiskMapMode.File:
                new_file = File(next_file_id)
                next_file_id += 1
                start_index = len(self.blocks)
                self.blocks.extend(new_file for _ in range(value))
                end_index = len(self.blocks)
                for index in range(start_index, end_index):
                    self.block_usage[index] = True
                self.files.add(new_file)

            if mode is DiskMapMode.FreeSpace:
                self.blocks.extend(None for _ in range(value))

            mode = ~mode

    def de_fragment(self) -> None:
        rightmost_used_block: int | None = None
        leftmost_unused_block: int | None = None
        while True:
            rightmost_used_block = self.block_usage.previous_set_bit_index(rightmost_used_block)
            leftmost_unused_block = self.block_usage.next_clear_bit_index(leftmost_unused_block)
            if rightmost_used_block == -1:
                return
            if rightmost_used_block < leftmost_unused_block:
                return

            self.blocks[leftmost_unused_block] = self.blocks[rightmost_used_block]
            self.blocks[rightmost_used_block] = None
            self.block_usage[leftmost_unused_block] = True
            self.block_usage[rightmost_used_block] = False

    def filesystem_checksum(self) -> int:
        accumulator = 0
        for index, file in enumerate(self.blocks):
            if file is None:
                break
            accumulator += index * file.id
        assert self.block_usage.next_set_bit_index(index) == -1
        return accumulator


class PartOneSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    def solve(self) -> int:
        disk = Disk(self.instance.disk_map)
        disk.de_fragment()
        return disk.filesystem_checksum()
