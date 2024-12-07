from .problem import ProblemInstance, Handful, Game


class PartTwoSolver:
    def __init__(self, instance: ProblemInstance) -> None:
        self.instance = instance

    @classmethod
    def game_minimum_bag(cls, game: Game) -> Handful:
        red = 0
        green = 0
        blue = 0
        for handful in game.history:
            if red < handful.red:
                red = handful.red
            if green < handful.green:
                green = handful.green
            if blue < handful.blue:
                blue = handful.blue
        return Handful(red=red, green=green, blue=blue)
    
    @classmethod
    def handful_power_set(cls, handful: Handful) -> int:
        return handful.red * handful.green * handful.blue

    def solve(self) -> int:
        minimum_bags = (self.game_minimum_bag(game) for game in self.instance.games)
        return sum(self.handful_power_set(minimum_bag) for minimum_bag in minimum_bags)
