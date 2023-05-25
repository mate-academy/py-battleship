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

        x_start = start[0]
        x_end = end[0]
        y_start = start[1]
        y_end = end[1]

        if y_start != y_end:
            if y_start - y_end < 0:
                self.decks = [
                    Deck(x_start, y)
                    for y in range(y_start, y_end + 1)
                ]
            else:
                self.decks = [
                    Deck(x_start, y)
                    for y in range(y_end, y_start + 1)
                ]
        else:
            if x_start - x_end < 0:
                self.decks = [
                    Deck(x, y_start)
                    for x in range(x_start, x_end + 1)
                ]
            else:
                self.decks = [
                    Deck(x, y_start)
                    for x in range(x_end, x_start + 1)
                ]

    def get_deck(self, row: int, column: int) -> Deck:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        self.get_deck(row, column).is_alive = False
        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True


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
            live_deck = ship.get_deck(*location).is_alive is True
            last_live_deck = [
                deck.is_alive
                for deck in ship.decks
            ].count(True) == 1
            if live_deck and last_live_deck:
                ship.fire(*location)
                return "Sunk!"
            else:
                ship.fire(*location)
                return "Hit!"
        else:
            return "Miss!"
