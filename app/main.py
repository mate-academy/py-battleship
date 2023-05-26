class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        # Create decks and save them to a list `self.decks`
        self.is_drowned = is_drowned

        x_start, x_end = sorted([start[0], end[0]])
        y_start, y_end = sorted([start[1], end[1]])

        self.decks = [
            Deck(x, y)
            for x in range(x_start, x_end + 1)
            for y in range(y_start, y_end + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        self.get_deck(row, column).is_alive = False
        self.is_drowned = all(deck.is_alive is False for deck in self.decks)


class Battleship:
    def __init__(self, ships: tuple[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        ships = [Ship(*ship) for ship in ships]
        self.field = {}
        for ship in ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if self.field.get(location):
            ship = self.field.get(location)
            live_deck = ship.get_deck(*location).is_alive
            ship.fire(*location)
            if live_deck and ship.is_drowned:
                return "Sunk!"
            else:
                ship.fire(*location)
                return "Hit!"
        else:
            return "Miss!"
