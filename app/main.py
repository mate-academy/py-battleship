class Deck:
    """A class to create ship deck."""

    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        """Constructs all the necessary attributes for Deck object."""
        self.row = row
        self.column = column
        self.is_alive = is_alive
        self.deck = row, column


class Ship:
    """A class to create a ship."""

    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        """Create decks and save them to a list `self.decks`"""
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_ship()

    def create_ship(self) -> list[Deck]:
        """Create ship (list of decks)"""
        ship_start = Deck(self.start[0], self.start[1])
        ship_end = Deck(self.end[0], self.end[1])
        row_difference = ship_end.row - ship_start.row
        column_difference = ship_end.column - ship_start.column

        if row_difference == 0 and column_difference == 0:
            return [ship_start]

        elif row_difference == 2:
            return [
                ship_start,
                Deck(ship_start.row + 1, ship_end.column),
                ship_end
            ]
        elif row_difference == 3:
            return [
                ship_start,
                Deck(ship_start.row + 1, ship_start.column),
                Deck(ship_start.row + 2, ship_start.column),
                ship_end
            ]
        elif column_difference == 2:
            return [
                ship_start,
                Deck(ship_start.row, ship_start.column + 1),
                ship_end
            ]
        elif column_difference == 3:
            return [
                ship_start,
                Deck(ship_start.row, ship_start.column + 1),
                Deck(ship_start.row, ship_start.column + 2),
                ship_end
            ]
        return [ship_start, ship_end]

    def get_deck(self, row: int, column: int) -> Deck:
        """Find the corresponding deck in the list."""
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        """
        Change the `is_alive` status of the deck
        and update the `is_drowned` value if it's needed.
        """
        self.get_deck(row, column).is_alive = False
        if not any([deck.is_alive for deck in self.decks]):
            self.is_drowned = True


class Battleship:
    """A class to create a field with given ships. """

    def __init__(self, ships: list[tuple]) -> None:
        """Create a dict `self.field`."""
        self.ships = ships
        self.field = self.get_field()

    def get_field(self) -> dict:
        """
        Return field dictionary.
        Its keys are tuples - the coordinates of the non-empty cells,
        a value for each cell is a reference to the ship
        which is located in it
        """
        field = {}
        for ship_coordinate in self.ships:
            ship = Ship(ship_coordinate[0], ship_coordinate[1])
            for deck in ship.decks:
                field[deck.deck] = ship
        return field

    def fire(self, location: tuple[int, int]) -> str:
        """Simulate a shot to cell."""
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
