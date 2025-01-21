from dataclasses import dataclass
from enum import Flag

from util.span import span

from .problem import ProblemInstance


class DiskMapMode(Flag):
    File = 0
    FreeSpace = 1


@dataclass(frozen=True)
class File:
    id: int


@dataclass
class BlockSpan:
    file: File | None
    span: span

    @property
    def is_free_space(self) -> bool:
        return self.file is None


class Disk:
    def __init__(self, disk_map: str) -> None:
        self.block_spans: list[BlockSpan] = []
        self.files: set[File] = set()

        mode: DiskMapMode = DiskMapMode.File
        next_file_id = 0
        next_block_index = 0
        for character in disk_map:
            value = int(character)

            if mode is DiskMapMode.File:
                new_file = File(next_file_id)
                self.files.add(new_file)
                next_file_id += 1
                self.block_spans.append(BlockSpan(new_file, span(next_block_index, next_block_index + value)))
                next_block_index += value

            if mode is DiskMapMode.FreeSpace:
                self.block_spans.append(BlockSpan(None, span(next_block_index, next_block_index + value)))
                next_block_index += value

            mode = ~mode

    def index_of_next_free_space_block_span_at_least_sized(self, size: int) -> int | None:
        cursor = 0
        while True:
            if cursor >= len(self.block_spans):
                return None
            block_span = self.block_spans[cursor]
            if not block_span.is_free_space:
                cursor += 1
                continue
            if len(block_span.span) < size:
                cursor += 1
                continue
            return cursor

    def index_of_last_file_block_span(self, from_index: int) -> int | None:
        cursor = from_index
        while True:
            if cursor < 0:
                return None
            block_span = self.block_spans[cursor]
            if not block_span.is_free_space:
                return cursor
            cursor -= 1

    def de_fragment(self) -> None:
        file_to_move_index: int = len(self.block_spans) - 1
        while True:
            file_to_move_index = self.index_of_last_file_block_span(file_to_move_index)
            if file_to_move_index is None:
                return

            file_to_move_block_span = self.block_spans[file_to_move_index]
            free_space_index = self.index_of_next_free_space_block_span_at_least_sized(len(file_to_move_block_span.span))
            if free_space_index is None or free_space_index > file_to_move_index:
                file_to_move_index -= 1
                continue

            free_space_block_span = self.block_spans[free_space_index]

            new_file_start_block_index = free_space_block_span.span.start
            new_file_end_block_index = free_space_block_span.span.start + len(file_to_move_block_span.span)
            new_file_block_index_span = span(new_file_start_block_index, new_file_end_block_index)

            new_free_space_start_block_index = new_file_end_block_index
            new_free_space_end_block_index = free_space_block_span.span.stop
            new_free_space_block_index_span = span(new_free_space_start_block_index, new_free_space_end_block_index)

            if len(new_free_space_block_index_span) == 0:
                self.block_spans[free_space_index] = BlockSpan(file_to_move_block_span.file, new_file_block_index_span)
            else:
                self.block_spans[free_space_index:free_space_index+1] = [
                    BlockSpan(file_to_move_block_span.file, new_file_block_index_span),
                    BlockSpan(None, new_free_space_block_index_span),
                ]
                file_to_move_index += 1

            file_to_move_block_span.file = None
            self.collect_free_space_near(file_to_move_index)
            file_to_move_index -= 1

    def collect_free_space_near(self, block_span_index: int) -> None:
        block_span = self.block_spans[block_span_index]
        if not block_span.is_free_space:
            return

        if block_span_index < len(self.block_spans) - 1:
            right_block_span = self.block_spans[block_span_index + 1]
            if right_block_span.is_free_space:
                del self.block_spans[block_span_index + 1]
                block_span.span = block_span.span.union(right_block_span.span)

        if block_span_index > 0:
            left_block_span = self.block_spans[block_span_index - 1]
            if left_block_span.is_free_space:
                del self.block_spans[block_span_index - 1]
                block_span.span = block_span.span.union(left_block_span.span)

    def filesystem_checksum(self) -> int:
        accumulator = 0
        for block_span in self.block_spans:
            if block_span.file is None:
                continue
            for block_index in block_span.span:
                accumulator += block_index * block_span.file.id
        return accumulator


class PartTwoSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    def solve(self) -> int:
        disk = Disk(self.instance.disk_map)
        disk.de_fragment()
        return disk.filesystem_checksum()
