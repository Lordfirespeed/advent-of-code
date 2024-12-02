from collections import defaultdict


class Solution:
    def __init__(self, inputLines):
        self.inputLines = inputLines
        self.rooms = defaultdict(lambda: list())
        self.completePaths = []
        self.partialPathsToConsider = [["start"]]

        self.construct_network()

    def construct_network(self):
        for line in self.inputLines:
            connectFrom, connectTo = line.split("-")
            self.rooms[connectFrom].append(connectTo)
            self.rooms[connectTo].append(connectFrom)

    def consider_partial_path(self, path):
        inRoom = path[-1]
        couldMoveTo = self.rooms[inRoom].copy()
        for visitedRoom in path:
            if visitedRoom.islower():
                try:
                    couldMoveTo.remove(visitedRoom)
                except ValueError:
                    pass

        newPaths = []
        for moveToRoom in couldMoveTo:
            newPath = path.copy()
            newPath.append(moveToRoom)
            newPaths.append(newPath)

        return newPaths

    def search_all_paths_exhaustively(self):
        while len(self.partialPathsToConsider) > 0:
            partialPath = self.partialPathsToConsider.pop(0)
            extendedPaths = self.consider_partial_path(partialPath)
            for extendedPath in extendedPaths:
                if extendedPath[-1] == "end":
                    self.completePaths.append(extendedPath)
                else:
                    self.partialPathsToConsider.append(extendedPath)

    def get_number_of_valid_paths(self):
        self.search_all_paths_exhaustively()
        return len(self.completePaths)


if __name__ == "__main__":
    with open(r"Input\2021day12\myinput.txt") as inputFile:
        inputLines = [line.strip() for line in inputFile.readlines()]

    solver = Solution(inputLines)
    result = solver.get_number_of_valid_paths()
    print(f"Number of valid paths: {result}")
