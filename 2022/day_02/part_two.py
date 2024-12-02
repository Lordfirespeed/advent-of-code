from enum import Enum, auto


class GameMove(Enum):
    Rock = auto()
    A = Rock

    Paper = auto()
    B = Paper

    Scissors = auto()
    C = Scissors


class GameOutcome(Enum):
    ElfWin = auto()
    X = ElfWin

    Draw = auto()
    Y = Draw

    IWin = auto()
    Z = IWin


class RockPaperScissorsGame:
    x_beats_y = {GameMove.Paper: GameMove.Rock, GameMove.Rock: GameMove.Scissors, GameMove.Scissors: GameMove.Paper}
    x_is_beaten_by_y = {value: key for key, value in x_beats_y.items()}
    move_scores = {GameMove.Rock: 1, GameMove.Paper: 2, GameMove.Scissors: 3}
    outcome_scores = {GameOutcome.ElfWin: 0, GameOutcome.Draw: 3, GameOutcome.IWin: 6}

    def __init__(self, game_string: str) -> None:
        a, b = game_string.split(" ")
        self.elf_plays = GameMove[a]
        self.target_outcome = GameOutcome[b]

    def outcome_score(self) -> int:
        return self.outcome_scores[self.target_outcome]

    def determine_my_move(self) -> GameMove:
        if self.target_outcome == GameOutcome.Draw:
            return self.elf_plays

        if self.target_outcome == GameOutcome.IWin:
            return self.x_is_beaten_by_y[self.elf_plays]

        if self.target_outcome == GameOutcome.ElfWin:
            return self.x_beats_y[self.elf_plays]

    def moves_score(self) -> int:
        return self.move_scores[self.determine_my_move()]

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
