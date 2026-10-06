class Deck:
    def __init__(
        self, row: int, column: int, is_alive: bool = True
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
        if start[0] != end[0] and start[1] != end[1]:
            raise ValueError("Ships must be horizontal or vertical.")
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, column, not is_drowned)
            for row in range(min(start[0], end[0]), max(start[0], end[0]) + 1)
            for column in range(
                min(start[1], end[1]), max(start[1], end[1]) + 1
            )
        ]

    def get_deck(self, row: int, column: int) -> Deck | None:
        return next(
            (deck for deck in self.decks
             if (deck.row, deck.column) == (row, column)),
            None,
        )

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is not None:
            deck.is_alive = False
            self.is_drowned = not any(deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(
        self, ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field: dict[tuple[int, int], Ship] = {}
        for ship in self.ships:
            for deck in ship.decks:
                location = (deck.row, deck.column)
                if location in self.field:
                    raise ValueError("Ships cannot overlap.")
                self.field[location] = ship
        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        ship = self.field.get(location)
        if ship is None or not ship.get_deck(*location).is_alive:
            return "Miss!"
        ship.fire(*location)
        return "Sunk!" if ship.is_drowned else "Hit!"

    def _validate_field(self) -> None:
        if sorted(len(ship.decks) for ship in self.ships) != [
            1, 1, 1, 1, 2, 2, 2, 3, 3, 4
        ]:
            raise ValueError(
                "The fleet must contain the ten prescribed ships."
            )
        for (row, column), ship in self.field.items():
            if not (0 <= row < 10 and 0 <= column < 10):
                raise ValueError("All ships must fit within the 10x10 field.")
            for row_offset in (-1, 0, 1):
                for column_offset in (-1, 0, 1):
                    neighbor = self.field.get(
                        (row + row_offset, column + column_offset)
                    )
                    if neighbor is not None and neighbor is not ship:
                        raise ValueError(
                            "Ships cannot touch, even diagonally."
                        )

    def print_field(self) -> None:
        for row in range(10):
            symbols = []
            for column in range(10):
                ship = self.field.get((row, column))
                if ship is None:
                    symbols.append("~")
                elif ship.is_drowned:
                    symbols.append("x")
                elif ship.get_deck(row, column).is_alive:
                    symbols.append("□")
                else:
                    symbols.append("*")
            print("\t".join(symbols))
