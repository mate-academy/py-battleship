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
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck:
        """Return the deck placed in the given cell."""
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

        raise ValueError(f"Ship has no deck in cell ({row}, {column})")

    def fire(self, row: int, column: int) -> None:
        """Damage the deck and drown the ship if it was the last one."""
        self.get_deck(row, column).is_alive = False

        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    FIELD_SIZE = 10
    SHIPS_BY_LENGTH = {1: 4, 2: 3, 3: 2, 4: 1}

    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}

        for start, end in ships:
            ship = Ship(start, end)

            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: tuple) -> str:
        """Shoot the cell and report the result."""
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        ship.fire(*location)

        return "Sunk!" if ship.is_drowned else "Hit!"

    def print_field(self) -> None:
        """Print the field row by row."""
        for row in range(self.FIELD_SIZE):
            cells = []

            for column in range(self.FIELD_SIZE):
                ship = self.field.get((row, column))

                if ship is None:
                    cells.append("~")
                elif ship.is_drowned:
                    cells.append("x")
                elif ship.get_deck(row, column).is_alive:
                    cells.append("\u25A1")
                else:
                    cells.append("*")

            print("\t".join(cells))

    def _validate_field(self) -> None:
        """Check the amount, the sizes and the placement of the ships."""
        ships = set(self.field.values())

        if len(ships) != 10:
            raise ValueError(
                f"The field should contain 10 ships, got {len(ships)}"
            )

        for length, amount in self.SHIPS_BY_LENGTH.items():
            actual = len([ship for ship in ships if len(ship.decks) == length])

            if actual != amount:
                raise ValueError(
                    f"The field should contain {amount} ships "
                    f"with {length} deck(s), got {actual}"
                )

        for (row, column), ship in self.field.items():
            for row_shift in (-1, 0, 1):
                for column_shift in (-1, 0, 1):
                    neighbour = (row + row_shift, column + column_shift)

                    if self.field.get(neighbour) not in (None, ship):
                        raise ValueError(
                            f"Ships in cells ({row}, {column}) and "
                            f"{neighbour} are neighbours"
                        )
