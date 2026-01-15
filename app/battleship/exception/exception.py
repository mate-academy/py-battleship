class BattleshipException(Exception):
    pass


class CloseLocationException(BattleshipException):
    def __init__(self, ship: str, closely_ship: str) -> None:
        super().__init__(
            f"The distance between the {ship} "
            f"and {closely_ship} should be 1 game cell"
        )


class WrongShipsNumber(BattleshipException):
    pass
