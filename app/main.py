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
        self.is_drowned = is_drowned
        self.decks: list[Deck] = []

        row1, col1 = start
        row2, col2 = end

        if row1 == row2:
            left = min(col1, col2)
            right = max(col1, col2)

            for column in range(left, right + 1):
                self.decks.append(Deck(row1, column))
        elif col1 == col2:
            top = min(row1, row2)
            bottom = max(row1, row2)

            for row in range(top, bottom + 1):
                self.decks.append(Deck(row, col1))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)

        if deck is None or not deck.is_alive:
            return

        deck.is_alive = False

        for current_deck in self.decks:
            if current_deck.is_alive:
                return

        self.is_drowned = True


class Battleship:
    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.ships = ships
        self.field: dict[tuple[int, int], Ship] = {}

        for start, end in ships:
            ship = Ship(start, end)

            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"

        row, column = location
        ship = self.field[location]
        deck = ship.get_deck(row, column)

        if deck is None or not deck.is_alive:
            return "Miss!"

        ship.fire(row, column)

        if ship.is_drowned:
            return "Sunk!"

        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            line = []

            for column in range(10):
                location = (row, column)

                if location not in self.field:
                    line.append("~")
                    continue

                ship = self.field[location]
                deck = ship.get_deck(row, column)

                if deck is None:
                    line.append("~")
                elif deck.is_alive:
                    line.append("□")
                elif ship.is_drowned:
                    line.append("x")
                else:
                    line.append("*")

            print(" ".join(line))

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("Invalid number of ships")

        ship_sizes: dict[int, int] = {}

        for start, end in self.ships:
            row1, col1 = start
            row2, col2 = end

            if row1 != row2 and col1 != col2:
                raise ValueError("Ship must be horizontal or vertical")

            if not (
                    0 <= row1 < 10
                    and 0 <= col1 < 10
                    and 0 <= row2 < 10
                    and 0 <= col2 < 10
            ):
                raise ValueError("Ship is out of field")

            size = max(abs(row2 - row1), abs(col2 - col1)) + 1
            ship_sizes[size] = ship_sizes.get(size, 0) + 1

        expected_sizes = {
            1: 4,
            2: 3,
            3: 2,
            4: 1,
        }

        if ship_sizes != expected_sizes:
            raise ValueError("Invalid ships configuration")

        occupied_cells = set(self.field.keys())

        for cell, ship in self.field.items():
            row, column = cell

            for row_diff in (-1, 0, 1):
                for column_diff in (-1, 0, 1):
                    if row_diff == 0 and column_diff == 0:
                        continue

                    neighbour = (row + row_diff, column + column_diff)

                    if neighbour not in occupied_cells:
                        continue

                    neighbour_ship = self.field[neighbour]

                    if neighbour_ship is not ship:
                        raise ValueError("Ships cannot touch each other")
