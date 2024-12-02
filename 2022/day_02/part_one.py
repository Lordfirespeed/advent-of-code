from enum import Enum, auto


class Moves(Enum):
    Rock = auto()
    A = Rock
    X = Rock

    Paper = auto()
    B = Paper
    Y = Paper

    Scissors = auto()
    C = Scissors
    Z = Scissors


class GameOutcome(Enum):
    ElfWin = auto()
    IWin = auto()
    Draw = auto()


class RockPaperScissorsGame:
    beats = {Moves.Paper: Moves.Rock, Moves.Rock: Moves.Scissors, Moves.Scissors: Moves.Paper}
    move_scores = {Moves.Rock: 1, Moves.Paper: 2, Moves.Scissors: 3}
    outcome_scores = {GameOutcome.ElfWin: 0, GameOutcome.Draw: 3, GameOutcome.IWin: 6}

    def __init__(self, game_string: str) -> None:
        a, b = game_string.split(" ")
        self.elf_plays = Moves[a]
        self.I_play = Moves[b]

    def outcome(self) -> GameOutcome:
        if self.elf_plays == self.I_play:
            return GameOutcome.Draw
        if self.beats[self.I_play] == self.elf_plays:
            return GameOutcome.IWin
        return GameOutcome.ElfWin

    def outcome_score(self) -> int:
        return self.outcome_scores[self.outcome()]

    def moves_score(self) -> int:
        return self.move_scores[self.I_play]

    def determine_score(self) -> int:
        return self.outcome_score() + self.moves_score()


class Solution:
    def __init__(self, input_lines):
        self.game_strings = input_lines
        self.games: [RockPaperScissorsGame] = None
        self.game_scores: [int] = None

    def total_score(self):
        self.games = map(RockPaperScissorsGame, self.game_strings)
        self.game_scores = map(lambda game: game.determine_score(), self.games)
        return sum(self.game_scores)


if __name__ == "__main__":
    with open(r"input.txt") as inputFile:
        input_lines = [line.strip() for line in inputFile.readlines()]

    solver = Solution(input_lines)
    result = solver.total_score()
    print(f"My total score was {result}")
