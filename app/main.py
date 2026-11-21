class Deck:
    def __init__(
        self,
        row: int,
        column: int,
        is_alive: bool = True,
    ) -> None:
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
        self.is_drowned = is_drowned
        self.decks: list[Deck] = []

        start_row, start_column = start
        end_row, end_column = end

        if start_row != end_row and start_column != end_column:
            raise ValueError("Ships must be horizontal or vertical")

        if start_row == end_row:
            first_column = min(start_column, end_column)
            last_column = max(start_column, end_column)

            for column in range(first_column, last_column + 1):
                self.decks.append(Deck(start_row, column))
        else:
            first_row = min(start_row, end_row)
            last_row = max(start_row, end_row)

            for row in range(first_row, last_row + 1):
                self.decks.append(Deck(row, start_column))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)

        if deck is None:
            return "Miss!"

        deck.is_alive = False
        self.is_drowned = all(
            not current_deck.is_alive
            for current_deck in self.decks
        )

        if self.is_drowned:
            return "Sunk!"

        return "Hit!"


class Battleship:
    FIELD_SIZE = 10

    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]],
    ) -> None:
        self.field: dict[tuple[int, int], Ship] = {}
        self.ships: list[Ship] = []

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)

            for deck in ship.decks:
                location = (deck.row, deck.column)

                if location in self.field:
                    raise ValueError("Ships cannot overlap")

                self.field[location] = ship

        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        self._validate_location(location)

        ship = self.field.get(location)

        if ship is None:
            return "Miss!"

        row, column = location
        return ship.fire(row, column)

    def print_field(self) -> None:
        for row in range(self.FIELD_SIZE):
            cells = []

            for column in range(self.FIELD_SIZE):
                ship = self.field.get((row, column))

                if ship is None:
                    cells.append("~")
                    continue

                deck = ship.get_deck(row, column)

                if ship.is_drowned:
                    cells.append("x")
                elif deck is not None and not deck.is_alive:
                    cells.append("*")
                else:
                    cells.append("\u25A1")

            print(" ".join(cells))

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("The field must contain exactly 10 ships")

        expected_ship_counts = {
            1: 4,
            2: 3,
            3: 2,
            4: 1,
        }

        actual_ship_counts = {
            size: sum(
                len(ship.decks) == size
                for ship in self.ships
            )
            for size in expected_ship_counts
        }

        if actual_ship_counts != expected_ship_counts:
            raise ValueError(
                "The field must contain 4 single-deck ships, "
                "3 double-deck ships, 2 three-deck ships, "
                "and 1 four-deck ship"
            )

        for ship in self.ships:
            for deck in ship.decks:
                self._validate_location((deck.row, deck.column))

        for index, first_ship in enumerate(self.ships):
            for second_ship in self.ships[index + 1:]:
                if self._ships_are_neighbors(
                    first_ship,
                    second_ship,
                ):
                    raise ValueError(
                        "Ships cannot be located in neighboring cells"
                    )

    def _ships_are_neighbors(
        self,
        first_ship: Ship,
        second_ship: Ship,
    ) -> bool:
        for first_deck in first_ship.decks:
            for second_deck in second_ship.decks:
                row_difference = abs(
                    first_deck.row - second_deck.row
                )
                column_difference = abs(
                    first_deck.column - second_deck.column
                )

                if row_difference <= 1 and column_difference <= 1:
                    return True

        return False

    def _validate_location(
        self,
        location: tuple[int, int],
    ) -> None:
        if len(location) != 2:
            raise ValueError("A location must contain row and column")

        row, column = location

        if not isinstance(row, int) or not isinstance(column, int):
            raise TypeError("Row and column must be integers")

        valid_row = 0 <= row < self.FIELD_SIZE
        valid_column = 0 <= column < self.FIELD_SIZE

        if not valid_row or not valid_column:
            raise ValueError(
                "Row and column must be between 0 and 9"
            )
