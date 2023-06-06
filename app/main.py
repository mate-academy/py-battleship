class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self, start: "Deck",
            end: "Deck",
            is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        if start.row == end.row and start.column == end.column:
            self.decks.append(Deck(start.row, start.column))
        elif start.row == end.row:
            for i in range(start.column, end.column + 1):
                self.decks.append(Deck(start.row, i))
        elif start.column == end.column:
            for i in range(start.row, end.row + 1):
                self.decks.append(Deck(i, start.column))

    def get_deck(self, row: int, column: int) -> "Deck":
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        raise ValueError("There is no such deck")

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        deck.is_alive = not deck.is_alive
        is_decks_alive = []
        for deck in self.decks:
            is_decks_alive.append(deck.is_alive)
        if any(is_decks_alive):
            self.is_drowned = False
        else:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        for ship in ships:
            new_ship = Ship(
                Deck(ship[0][0], ship[0][1]),
                Deck(ship[1][0], ship[1][1])
            )
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

    def print_field(self) -> None:
        matrix = []
        for i in range(0, 10):
            row = []
            for jj in range(0, 10):
                if (i, jj) in self.field:
                    ship = self.field[(i, jj)]
                    if ship.is_drowned:
                        row.append("x")
                    else:
                        deck = ship.get_deck(i, jj)
                        row.append("o") if deck.is_alive else row.append("*")
                else:
                    row.append("~")
            matrix.append(row)

        for row in matrix:
            print(" ".join(row))
        return matrix

    def fire(self, location: tuple) -> None:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
