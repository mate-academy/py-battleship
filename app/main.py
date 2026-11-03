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
        is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, column)
            for row in range(min(start[0], end[0]), max(start[0], end[0]) + 1)
            for column in range(
                min(start[1], end[1]), max(start[1], end[1]) + 1
            )
        ]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    FIELD_SIZE = 10
    EXPECTED_SHIPS = {1: 4, 2: 3, 3: 2, 4: 1}

    def __init__(self, ships: list) -> None:
        self.field = {}
        self.ships = [Ship(start, end) for start, end in ships]
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship
        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        ship.fire(*location)
        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        for row in range(self.FIELD_SIZE):
            symbols = [
                self._get_cell_symbol(row, column)
                for column in range(self.FIELD_SIZE)
            ]
            print("\t".join(symbols))

    def _get_cell_symbol(self, row: int, column: int) -> str:
        ship = self.field.get((row, column))
        if ship is None:
            return "~"
        if ship.is_drowned:
            return "x"
        if not ship.get_deck(row, column).is_alive:
            return "*"
        return "\u25A1"

    def _validate_field(self) -> None:
        if len(self.ships) != sum(self.EXPECTED_SHIPS.values()):
            raise ValueError("The total number of ships should be 10")

        ship_sizes = {}
        for ship in self.ships:
            size = len(ship.decks)
            ship_sizes[size] = ship_sizes.get(size, 0) + 1
        if ship_sizes != self.EXPECTED_SHIPS:
            raise ValueError(
                "There should be 4 single-deck, 3 double-deck, "
                "2 three-deck and 1 four-deck ships"
            )

        for ship in self.ships:
            if self._has_foreign_neighbor(ship):
                raise ValueError("Ships shouldn't be in neighboring cells")

    def _has_foreign_neighbor(self, ship: Ship) -> bool:
        for deck in ship.decks:
            for row_shift in (-1, 0, 1):
                for column_shift in (-1, 0, 1):
                    cell = (deck.row + row_shift, deck.column + column_shift)
                    if self.field.get(cell, ship) is not ship:
                        return True
        return False
