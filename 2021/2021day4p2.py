class BingoNumber:
    def __init__(self, number):
        self.number = number
        self.called = False

    def __eq__(self, other):
        if type(other) == BingoNumber:
            return other.number == self.number
        elif type(other) == int:
            return other == self.number
        else:
            raise TypeError


class BingoBoard:
    def __init__(self, board):
        self.board = [[BingoNumber(num) for num in row] for row in board]
        self.won = False

    def onNumberCalled(self, number):
        for row in self.board:
            for num in row:
                if num == number:
                    num.called = True

    def checkWon(self):
        self.won = False
        for row in self.board:
            if all([num.called for num in row]):
                self.won = True

        rotated = list(zip(*self.board))
        for column in rotated:
            if all([num.called for num in column]):
                self.won = True

        return self.won


class BingoGame:
    def __init__(self, players):
        self.players = players
        self.called = []
        self.played = False
        self.winner = None
        self.wonAt = None

    def callNumber(self, number):
        for player in self.players:
            player.onNumberCalled(number)

    def checkWinners(self):
        for player in self.players:
            if not player.won:
                won = player.checkWon()
                if won:
                    self.winner = player
                    self.wonAt = len(self.called) - 1

    def playGame(self, callouts):
        if not self.played:
            self.played = True
            while not all([player.won for player in self.players]) and len(callouts) > 0:
                toCall = callouts.pop(0)
                self.callNumber(toCall)
                self.called.append(toCall)
                self.checkWinners()

        return self.winner


if __name__ == "__main__":
    with open(r"Input\2021day4.txt") as inputFile:
        inputFileString = "".join([line for line in inputFile.readlines()])

    stringBoardsMultiLine = inputFileString.split("\n\n")
    picked = [int(num) for num in stringBoardsMultiLine[0].split(",")]

    stringRowBoards = [board.split("\n") for board in stringBoardsMultiLine[1:]]
    numBoard2dArrays = [[[int(num) for num in boardRow.split()] for boardRow in board] for board in stringRowBoards]

    players = [BingoBoard(board) for board in numBoard2dArrays]
    game = BingoGame(players)
    winner = game.playGame(picked)
    justCalled = game.called[game.wonAt]

    notCalled = [num.number for row in winner.board for num in row if not num.called]
    result = sum(notCalled) * justCalled
    print(f"Sum of winner's unmarked numbers: {result}")
