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
            is_drowned: bool = False) -> None:
        # Create decks and save them to a list `self.decks`
        self.is_drowned = is_drowned
        self.decks = []
        # If the ship is placed horizontally - axis = 0, vertically - 1
        axis = 0 if start[0] != end[0] else 1
        for deck in range(start[axis], end[axis] + 1):
            if axis:
                self.decks.append(Deck(start[0], deck))
            else:
                self.decks.append(Deck(deck, start[1]))
        self.hitpoints = len(self.decks)

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck
        raise ValueError(
            f"No such deck with coordinates: row {row}, column {column}")

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        target = self.get_deck(row, column)
        target.is_alive = False
        self.hitpoints -= 1
        if self.hitpoints == 0:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        for ship in ships:
            self.field[ship] = Ship(ship[0], ship[1])
        self.battlefield = []
        self.set_battlefield()
        self.deploy_ships()

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        for ship in self.field.values():
            for deck in ship.decks:
                if (deck.row, deck.column) == location:
                    ship.fire(location[0], location[1])
                    if not ship.is_drowned:
                        return "Hit!"
                    else:
                        return "Sunk!"
        return "Miss!"

    def set_battlefield(self) -> None:
        for row in range(10):
            self.battlefield.append([])
            for _ in range(10):
                self.battlefield[row].append("~")

    def deploy_ships(self) -> None:
        for ship in self.field.values():
            for deck in ship.decks:
                self.battlefield[deck.row][deck.column] = u"\u25A1"

    def print_field(self) -> str:
        to_print = self.battlefield.copy()
        to_print = "\n".join(["".join(row) for row in to_print])
        return to_print


if __name__ == "__main__":
    pass
