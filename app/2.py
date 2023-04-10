class Deck:
    def __init__(self, row: tuple, column: tuple, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        # Create decks and save them to a list `self.decks`

    def get_deck(self, row: tuple, column: tuple) -> None:

        # Find the corresponding deck in the list

    def fire(self, row: tuple, column: tuple) -> None:
    # Change the `is_alive` status of the deck
    # And update the `is_drowned` value if it's needed

class Battleship:
    def __init__(self, ships: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
        self.ships = ships
        self.field = {}
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        pass

    def fire(self, ceil: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
