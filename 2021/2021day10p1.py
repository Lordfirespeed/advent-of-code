class ChunkCorrupted(Exception):
    """Raised when chunk is corrupted"""
    def __init__(self, illegalCharacter):
        self.illegalCharacter = illegalCharacter
        super(ChunkCorrupted, self).__init__()


class Chunk:
    legalChunkEnds = {")": "(", "]": "[", "}": "{", ">": "<"}

    def __init__(self, chunkString):
        self.chunkString = chunkString
        self.validate()

    def validate(self):
        openers = []
        for character in self.chunkString:
            if character in self.legalChunkEnds.keys():
                if openers[0] == self.legalChunkEnds[character]:
                    openers.pop(0)
                else:
                    raise ChunkCorrupted(character)
            else:
                openers.insert(0, character)


class Solution:
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}

    def __init__(self, inputLines):
        self.chunkStrings = inputLines

    def get_total_syntax_score_for_corrupted_chunks(self):
        syntaxScore = 0

        for chunkString in self.chunkStrings:
            try:
                Chunk(chunkString)
            except ChunkCorrupted as corruptedError:
                syntaxScore += self.scores[corruptedError.illegalCharacter]

        return syntaxScore


if __name__ == "__main__":
    with open(r"Input\2021day10.txt") as inputFile:
        inputLines = [line.strip() for line in inputFile.readlines()]

    solver = Solution(inputLines)
    result = solver.get_total_syntax_score_for_corrupted_chunks()
    print(f"Total syntax score: {result}")
