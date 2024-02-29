class BattleshipException(Exception):
    def __init__(self, message="Battleship exception") -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class TotalNumberOfShips(BattleshipException):
    pass


class NumberOfDecks(BattleshipException):
    pass


class NumberOfShips(BattleshipException):
    pass


class CloseShips(BattleshipException):
    pass
