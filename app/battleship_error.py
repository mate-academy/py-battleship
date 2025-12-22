class BattleShipError(Exception):
    pass


class TotalShipsAmountError(BattleShipError):
    def __init__(
            self,
            message: str = "Total amount of ships should be 10"
    ) -> None:
        super().__init__(message)


class DeckAmountError(BattleShipError):
    def __init__(
            self,
            amount_of_ships: int,
            amount_of_decks: int,
            actual: int
    ) -> None:
        super().__init__(
            f"There should be {amount_of_ships} "
            f"{amount_of_decks}-deck ships, "
            f"{actual} instead"
        )


class LocationError(BattleShipError):
    def __init__(
            self,
            message: str = "Ships shouldn't be located in the neighbor cells"
    ) -> None:
        super().__init__(message)
