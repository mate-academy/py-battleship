class ShipsCountException(Exception):
    default_message = "ShipsCountException: Total number of ships should be 10"

    def __init__(self, msg: str = default_message) -> None:
        super().__init__(msg)


class ShipsTypesException(Exception):

    default_message = (
        "There should be 4 single-deck ships, "
        "3 double-deck ships, "
        "2 three-deck ships and "
        "1 four-deck ship"
    )

    def __init__(self, msg: str = default_message) -> None:
        super().__init__(msg)


class ShipsAreNeighboursException(Exception):
    default_message = "Ships shouldn't be located in the neighboring cells"

    def __init__(self, msg: str = default_message) -> None:
        super().__init__(msg)
