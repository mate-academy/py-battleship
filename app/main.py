class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        start_x, start_y = start
        end_x, end_y = end
        self.decks = []
        if start_x == end_x:  # Horizontal
            for y_coord in range(start_y, end_y + 1):
                deck = Deck(start_x, y_coord)
                self.decks.append(deck)
        elif start_y == end_y:  # Vertical
            for x_coord in range(start_x, end_x + 1):
                deck = Deck(x_coord, start_y)
                self.decks.append(deck)

        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False

        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        for ship_coords in ships:
            start, end = ship_coords
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        ship.fire(*location)
        if ship.is_drowned:
            return "Sunk!"
        else:
            return "Hit!"
