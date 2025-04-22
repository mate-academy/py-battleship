class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            ship: "Ship",
            is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.ship = ship
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks = []
        self.is_drowned = is_drowned

        x1, y1 = start
        x2, y2 = end

        if x1 == x2:  # vertical line
            for i in range(y1, y2 + 1):
                self.decks.append(Deck(x1, i, self))
        elif y1 == y2:  # horizontal line
            for i in range(x1, x2 + 1):
                self.decks.append(Deck(i, y1, self))

    def get_deck(self, row: int, column: int) -> Deck or None:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        self.get_deck(row, column).is_alive = False
        deck_remaining = False
        for deck in self.decks:
            if deck.is_alive:
                deck_remaining = True
                break
        if not deck_remaining:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        for cords in ships:
            start, end = cords
            ship = Ship(start, end)

            x1, y1 = start
            x2, y2 = end

            if x1 == x2:  # vertical line
                for i in range(y1, y2 + 1):
                    self.field[(x1, i)] = ship
            elif y1 == y2:  # horizontal line
                for i in range(x1, x2 + 1):
                    self.field[(i, y1)] = ship

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            x, y = location
            target = self.field[(x, y)]
            target.fire(x, y)
            if target.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        else:
            return "Miss!"
