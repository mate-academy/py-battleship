class BattleshipException(Exception):
    def __init__(self, message: str = "Battleship exception") -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class ShipPlacementExeption(BattleshipException):
    pass


class TotalShipsInFleet(BattleshipException):
    pass


class NumberOfShips(BattleshipException):
    pass


class CloseShips(BattleshipException):
    pass
