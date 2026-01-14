class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
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
        self.decks = []
        for column in range(start[0], end[0] + 1):
            for row in range(start[1], end[1] + 1):
                self.decks.append(
                    Deck(column, row)
                )
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def check_ship(self) -> bool:
        for deck in self.decks:
            if deck.is_alive:
                return True
        return False

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        if deck is None:
            return
        deck.is_alive = False
        self.is_drowned = self.check_ship()


class Battleship:
    def __init__(self, ships: tuple[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {
            ship: Ship(
                ship[0], ship[1]
            )
            for ship in ships
        }

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        for ship in self.field.values():
            if ship.get_deck(*location):
                ship.fire(*location)
                if ship.is_drowned:
                    return "Hit!"
                else:
                    return "Sunk!"
        return "Miss!"
