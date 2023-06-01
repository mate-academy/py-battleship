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
        self.decks = [
            Deck(row, column) for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        this_deck = self.get_deck(row, column)
        if this_deck.is_alive:
            this_deck.is_alive = False
            if not any(deck.is_alive for deck in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {
            (row, column): None for column in range(10) for row in range(10)
        }
        for ship in ships:
            current_ship = Ship(*ship)
            for deck in current_ship.decks:
                self.field[(deck.row, deck.column)] = current_ship

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if self.field[location]:
            self.field[location].fire(*location)
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                ship = self.field[(row, column)]
                if ship is None:
                    print("~", "\t", end="")
                elif ship.is_drowned:
                    print("x", "\t", end="")
                elif (not ship.is_drowned
                      and ship.get_deck(row, column).is_alive):
                    print("□", "\t", end="")
                else:
                    print("*", "\t", end="")
            print("")
