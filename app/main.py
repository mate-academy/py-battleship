from __future__ import annotations


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
        self.decks = []

        start_row, start_column = start
        end_row, end_column = end

        if start_row != end_row and start_column != end_column:
            raise ValueError("Ships must be horizontal or vertical.")

        for row in range(min(start_row, end_row),
                         max(start_row, end_row) + 1):
            for column in range(min(start_column, end_column),
                                max(start_column, end_column) + 1):
                if not (0 <= row < 10 and 0 <= column < 10):
                    raise ValueError("Ship coordinates must be in the field.")
                self.decks.append(
                    Deck(row, column, is_alive=not is_drowned)
                )

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is not None:
            deck.is_alive = False
            self.is_drowned = all(
                not item.is_alive for item in self.decks
            )


class Battleship:
    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]],
    ) -> None:
        self.field = {}

        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                location = (deck.row, deck.column)
                if location in self.field:
                    raise ValueError("Ships must not overlap.")
                self.field[location] = ship

    def fire(self, location: tuple[int, int]) -> str:
        ship = self.field.get(location)
        if ship is None:
            return "Miss!"

        deck = ship.get_deck(*location)
        if deck is None or not deck.is_alive:
            return "Miss!"

        ship.fire(*location)
        return "Sunk!" if ship.is_drowned else "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            cells = []
            for column in range(10):
                ship = self.field.get((row, column))

                if ship is None:
                    cells.append("~")
                elif ship.is_drowned:
                    cells.append("x")
                else:
                    deck = ship.get_deck(row, column)
                    cells.append("□" if deck.is_alive else "*")

            print("\t".join(cells))

    def _validate_field(self) -> None:
        ships = set(self.field.values())
        counts = {
            size: sum(len(ship.decks) == size for ship in ships)
            for size in range(1, 5)
        }

        if len(ships) != 10 or counts != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValueError("Invalid fleet composition.")

        for (row, column), ship in self.field.items():
            for row_offset in (-1, 0, 1):
                for column_offset in (-1, 0, 1):
                    neighbor = self.field.get(
                        (row + row_offset, column + column_offset)
                    )
                    if neighbor is not None and neighbor is not ship:
                        raise ValueError("Ships must not touch.")
