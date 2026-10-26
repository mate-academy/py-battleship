class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        is_drowned: bool = False,
    ) -> None:
        self.decks = []
        self.is_drowned = is_drowned
        start_row, start_column = start
        end_row, end_column = end

        coordinates = (start_row, start_column, end_row, end_column)
        if any(not isinstance(value, int) for value in coordinates):
            raise ValueError("Ship coordinates must be integers")
        if any(not 0 <= value < 10 for value in coordinates):
            raise ValueError(
                "Ship coordinates must be inside the 10x10 field"
            )

        if start_row != end_row and start_column != end_column:
            raise ValueError(
                "A ship must be placed horizontally or vertically"
            )

        row_step = (end_row > start_row) - (end_row < start_row)
        column_step = (end_column > start_column) - (
            end_column < start_column
        )
        row, column = start_row, start_column
        while True:
            self.decks.append(Deck(row, column))
            if (row, column) == (end_row, end_column):
                break
            row += row_step
            column += column_step

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck is None or not deck.is_alive:
            return "Miss!"

        deck.is_alive = False
        self.is_drowned = not any(item.is_alive for item in self.decks)
        return "Sunk!" if self.is_drowned else "Hit!"


class Battleship:
    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]],
    ) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = {}
        for ship in self.ships:
            for deck in ship.decks:
                location = (deck.row, deck.column)
                if location in self.field:
                    raise ValueError("Ships cannot overlap")
                self.field[location] = ship
        self._validate_field()

    def _validate_field(self) -> None:
        """Check the standard fleet composition and ship separation."""
        lengths = [len(ship.decks) for ship in self.ships]
        if sorted(lengths) != [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]:
            raise ValueError("Fleet must contain 4 single, 3 double, "
                             "2 three, and 1 four-deck ships")

        for location, ship in self.field.items():
            row, column = location
            for neighbor_row in range(max(0, row - 1), min(9, row + 1) + 1):
                for neighbor_column in range(
                    max(0, column - 1), min(9, column + 1) + 1
                ):
                    neighbor = self.field.get((neighbor_row, neighbor_column))
                    if neighbor is not None and neighbor is not ship:
                        raise ValueError("Ships cannot touch, even diagonally")

    def fire(self, location: tuple[int, int]) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        ship = self.field.get(location)
        if ship is None:
            return "Miss!"
        row, column = location
        return ship.fire(row, column)

    def print_field(self) -> None:
        """Print the current 10x10 field using the README symbols."""
        for row in range(10):
            cells = []
            for column in range(10):
                ship = self.field.get((row, column))
                if ship is None:
                    cells.append("~")
                    continue
                deck = ship.get_deck(row, column)
                if ship.is_drowned:
                    cells.append("x")
                elif deck.is_alive:
                    cells.append("□")
                else:
                    cells.append("*")
            print("\t".join(cells))
