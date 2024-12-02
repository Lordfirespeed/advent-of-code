from copy import deepcopy
from collections import defaultdict


class CircularArray:
    def __init__(self, iterable):
        if type(iterable) is not list:
            raise NotImplementedError

        self.array = deepcopy(iterable)

    def __len__(self):
        return len(self.array)

    def __getitem__(self, item):
        if type(item) is not int:
            raise ValueError

        return self.array[self.__normalise_index(item)]

    def __repr__(self):
        return self.array.__repr__()

    def __normalise_index(self, index):
        if index < 0:
            return self.__normalise_index(len(self) + index)
        else:
            return index % len(self)

    def pop(self, index):
        if type(index) is not int:
            raise ValueError

        return self.array.pop(self.__normalise_index(index))

    def insert(self, index, item):
        if type(index) is not int:
            raise ValueError

        insertToIndex = self.__normalise_index(index)
        if insertToIndex == 0:
            insertToIndex = len(self)

        self.array.insert(insertToIndex, item)

        return insertToIndex


class MarbleGame:
    def __init__(self, players):
        self.players = players
        self.playerScores = defaultdict(lambda: 0)
        self.marbles = CircularArray([0])
        self.currentMarblePointer = 0
        self.currentTurnPlayerIndex = 0
        self.nextMarbleValue = 1
        self.played = False

    def get_highest_score(self):
        if not self.played:
            raise RuntimeError("Haven't played yet")

        return max(self.playerScores.values())

    def play_to_last_marble_worth(self, lastMarbleWorth):
        if self.played:
            raise RuntimeError("Already played")
        self.played = True

        while self.nextMarbleValue <= lastMarbleWorth:
            self.do_turn_and_increment_values()
            print(self.currentTurnPlayerIndex, self.marbles)

    def do_turn_and_increment_values(self):
        self.do_turn()
        self.currentTurnPlayerIndex += 1
        self.currentTurnPlayerIndex %= self.players
        self.nextMarbleValue += 1
        self.currentMarblePointer %= len(self.marbles)

    def do_turn(self):
        if self.nextMarbleValue % 23:
            self.do_normal_turn()
        else:
            self.do_23_turn()

    def do_normal_turn(self):
        newPointerPosition = self.marbles.insert(self.currentMarblePointer + 2, self.nextMarbleValue)
        self.currentMarblePointer = newPointerPosition

    def do_23_turn(self):
        self.playerScores[self.currentTurnPlayerIndex] += self.nextMarbleValue
        self.playerScores[self.currentTurnPlayerIndex] += self.marbles.pop(self.currentMarblePointer - 7)
        self.currentMarblePointer = self.currentMarblePointer - 7


if __name__ == "__main__":
    players = 4
    lastMarbleWorth = 192

    game = MarbleGame(players)
    game.play_to_last_marble_worth(lastMarbleWorth)
    result = game.get_highest_score()
    print(f"Highest Score: {result}")
