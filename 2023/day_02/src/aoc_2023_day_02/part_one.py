from .problem import ProblemInstance, Handful, Game


class PartOneSolver:
    bag = Handful(red=12, green=13, blue=14)

    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    @classmethod
    def handful_is_possible(cls, handful: Handful) -> bool:
        return handful.red <= cls.bag.red and handful.blue <= cls.bag.blue and handful.green <= cls.bag.green

    @classmethod
    def game_is_possible(cls, game: Game) -> bool:
        return all(cls.handful_is_possible(handful) for handful in game.history)

    def solve(self) -> int:
        return sum(game.game_id for game in self.instance.games if self.game_is_possible(game))
