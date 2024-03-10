class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:
        self.location = (row, column)
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        x_coords = [x for x in range(start[0], end[0] + 1)]
        y_coords = [y for y in range(start[1], end[1] + 1)]
        self.decks = [Deck(x, y) for x in x_coords for y in y_coords]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> int:
        for deck in self.decks:
            if deck.location == (row, column):
                return self.decks.index(deck)

    def fire(self, row: int, column: int) -> None:
        deck_index = self.get_deck(row, column)
        self.decks[deck_index].is_alive = False
        if not [1 for deck in self.decks if deck.is_alive]:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        pass

    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        pass