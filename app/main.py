FIELD_SIZE = 10
EXPECTED_SHIPS = {1: 4, 2: 3, 3: 2, 4: 1}

EMPTY_SYMBOL = "~"
ALIVE_DECK_SYMBOL = "\u25A1"
HIT_DECK_SYMBOL = "*"
DROWNED_DECK_SYMBOL = "x"


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        self.decks = [
            Deck(row, column)
            for row in range(min(start[0], end[0]), max(start[0], end[0]) + 1)
            for column in range(
                min(start[1], end[1]), max(start[1], end[1]) + 1
            )
        ]

    @property
    def is_drowned(self) -> bool:
        return not any(deck.is_alive for deck in self.decks)

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        deck.is_alive = False

        return "Sunk!" if self.is_drowned else "Hit!"


class Battleship:
    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]],
    ) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = {
            (deck.row, deck.column): ship
            for ship in self.ships
            for deck in ship.decks
        }
        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        ship = self.field.get(location)

        if ship is None:
            return "Miss!"

        return ship.fire(*location)

    def print_field(self) -> None:
        for row in range(FIELD_SIZE):
            symbols = [
                self._get_symbol(row, column) for column in range(FIELD_SIZE)
            ]
            print("  ".join(symbols))

    def _get_symbol(self, row: int, column: int) -> str:
        ship = self.field.get((row, column))

        if ship is None:
            return EMPTY_SYMBOL
        if ship.is_drowned:
            return DROWNED_DECK_SYMBOL
        if ship.get_deck(row, column).is_alive:
            return ALIVE_DECK_SYMBOL
        return HIT_DECK_SYMBOL

    def _validate_field(self) -> None:
        if len(self.ships) != sum(EXPECTED_SHIPS.values()):
            raise ValueError("The total number of the ships should be 10")

        sizes: dict[int, int] = {}
        for ship in self.ships:
            size = len(ship.decks)
            sizes[size] = sizes.get(size, 0) + 1

        if sizes != EXPECTED_SHIPS:
            raise ValueError(
                "There should be 4 single-deck, 3 double-deck, "
                "2 three-deck and 1 four-deck ships"
            )

        for ship in self.ships:
            for deck in ship.decks:
                for row_shift in (-1, 0, 1):
                    for column_shift in (-1, 0, 1):
                        neighbor = self.field.get(
                            (deck.row + row_shift, deck.column + column_shift)
                        )
                        if neighbor is not None and neighbor is not ship:
                            raise ValueError(
                                "Ships shouldn't be in the neighboring cells"
                            )
