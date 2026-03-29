class ShipCreationError(Exception):
    def __init__(self) -> None:
        message = "Can't create field with ships quantity less then 10"
        super().__init__(message)


class NominalShipError(Exception):
    def __init__(self) -> None:
        message = (
            "Please, check nominal of ships decks\n"
            "Suppose to have:\n"
            "One-deck ships = 4\n"
            "Two-deck ships = 3\n"
            "Three-deck ships = 2\n"
            "Four-deck ships = 1\n"
        )
        super().__init__(message)


class WrongCoordinatesError(Exception):
    def __init__(self) -> None:
        message = ("Can't create ship with such coordinates."
                   " Check the coordinates-list, please")
        super().__init__(message)


class CanNotBeNeighbourError(Exception):
    def __init__(self) -> None:
        message = "Can't create field, where ships are in neighbour cells"
        super().__init__(message)
