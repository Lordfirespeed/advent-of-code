class ChunkCorrupted(Exception):
    """Raised when chunk is corrupted"""
    def __init__(self, illegalCharacter):
        self.illegalCharacter = illegalCharacter
        super(ChunkCorrupted, self).__init__()


class Chunk:
    legalChunkEndsToStartsMap = {")": "(", "]": "[", "}": "{", ">": "<"}
    legalChunkStartsToEndsMap = {"(": ")", "[": "]", "{": "}", "<": ">"}

    def __init__(self, chunkString):
        self.chunkString = chunkString
        self.openers = []
        self.completionString = ""
        self.validate()

    def validate(self):
        for character in self.chunkString:
            if character in self.legalChunkEndsToStartsMap.keys():
                if self.openers[0] == self.legalChunkEndsToStartsMap[character]:
                    self.openers.pop(0)
                else:
                    raise ChunkCorrupted(character)
            else:
                self.openers.insert(0, character)

    def repair(self):
        self.completionString = "".join([self.legalChunkStartsToEndsMap[character] for character in self.openers])

    def __repr__(self):
        return f"Chunk:{self.chunkString}:"


class Solution:
    scores = {")": 1, "]": 2, "}": 3, ">": 4}

    def __init__(self, inputLines):
        self.chunkStrings = inputLines

    def get_autocomplete_score(self, chunk: Chunk):
        chunk.repair()
        score = 0
        for character in chunk.completionString:
            score *= 5
            score += self.scores[character]

        return score

    def get_middle_autocomplete_score(self):
        autocompleteScores = []

        for chunkString in self.chunkStrings:
            try:
                validatedChunk = Chunk(chunkString)
                autocompleteScores.append(self.get_autocomplete_score(validatedChunk))
            except ChunkCorrupted as corruptedError:
                pass

        autocompleteScores.sort()
        middleIndex = (len(autocompleteScores) - 1) // 2
        return autocompleteScores[middleIndex]


if __name__ == "__main__":
    with open(r"Input\2021day10.txt") as inputFile:
        inputLines = [line.strip() for line in inputFile.readlines()]

    solver = Solution(inputLines)
    result = solver.get_middle_autocomplete_score()
    print(f"Middle autocomplete score: {result}")
