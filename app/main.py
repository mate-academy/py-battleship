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
        is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks: list[Deck] = []
        self.is_drowned = is_drowned

        start_row, start_column = start
        end_row, end_column = end

        if start_row != end_row and start_column != end_column:
            raise ValueError(
                "Ship must be placed horizontally or vertically."
            )

        # Create decks for the ship
        if start_row == end_row:
            # Horizontal ship
            for column in range(
                min(start_column, end_column),
                max(start_column, end_column) + 1
            ):
                self.decks.append(Deck(start_row, column))
        else:
            # Vertical ship
            for row in range(
                min(start_row, end_row),
                max(start_row, end_row) + 1
            ):
                self.decks.append(Deck(row, start_column))

    def get_deck(self, row: int, column: int) -> Deck:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        raise ValueError("Deck not found.")

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        deck.is_alive = False

        self.is_drowned = all(
            not deck.is_alive for deck in self.decks
        )


class Battleship:
    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]],
    ) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field: dict[tuple[int, int], Ship] = {}

        for start, end in ships:
            ship = Ship(start, end)

            for deck in ship.decks:
                location = (deck.row, deck.column)
                self.field[location] = ship

        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        row, column = location

        deck = ship.get_deck(row, column)

        if not deck.is_alive:
            return "Sunk!" if ship.is_drowned else "Hit!"

        ship.fire(row, column)

        if ship.is_drowned:
            return "Sunk!"

        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            cells = []

            for column in range(10):
                location = (row, column)

                if location not in self.field:
                    cells.append("~")
                    continue

                ship = self.field[location]
                deck = ship.get_deck(row, column)

                if ship.is_drowned:
                    cells.append("x")
                elif deck.is_alive:
                    cells.append("□")
                else:
                    cells.append("*")

            print("\t".join(cells))

    def _validate_field(self) -> None:
        ship_lengths = [
            len(ship.decks)
            for ship in {
                id(ship): ship for ship in self.field.values()
            }.values()
        ]

        expected_lengths = {
            1: 4,
            2: 3,
            3: 2,
            4: 1,
        }

        if len(ship_lengths) != 10:
            raise ValueError("There must be exactly 10 ships")

        for length, expected_count in expected_lengths.items():
            if ship_lengths.count(length) != expected_count:
                raise ValueError("Invalid ship lengths")

        if any(
            not (0 <= row < 10 and 0 <= column < 10)
            for row, column in self.field
        ):
            raise ValueError("Ship is outside the field")

        for (row, column), ship in self.field.items():
            for row_offset in (-1, 0, 1):
                for column_offset in (-1, 0, 1):
                    if row_offset == 0 and column_offset == 0:
                        continue

                    neighbor = (
                        row + row_offset,
                        column + column_offset,
                    )

                    if neighbor not in self.field:
                        continue

                    if self.field[neighbor] is not ship:
                        raise ValueError("Ships cannot touch")
