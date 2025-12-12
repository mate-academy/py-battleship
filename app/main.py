from __future__ import annotations

from typing import Optional


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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks: list[Deck] = self._build_decks(start, end)

    def _build_decks(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
    ) -> list[Deck]:
        row_1, col_1 = start
        row_2, col_2 = end

        if start == end:
            return [Deck(row_1, col_1)]

        if row_1 == row_2:
            col_start, col_end = sorted((col_1, col_2))
            return [Deck(row_1, col) for col in range(col_start, col_end + 1)]

        if col_1 == col_2:
            row_start, row_end = sorted((row_1, row_2))
            return [Deck(row, col_1) for row in range(row_start, row_end + 1)]

        raise ValueError(f"Ship must be straight: {start} -> {end}")

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is None:
            return

        deck.is_alive = False
        self.is_drowned = all(
            not deck_item.is_alive for deck_item in self.decks
        )


class Battleship:
    size = 10

    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]],
    ) -> None:
        self.ships: list[Ship] = []
        self.field: dict[tuple[int, int], Ship] = {}

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)

            for deck in ship.decks:
                cell = (deck.row, deck.column)
                if cell in self.field:
                    raise ValueError(f"Overlapping ships at {cell}")
                self.field[cell] = ship

        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        row, col = location

        if not (0 <= row < self.size and 0 <= col < self.size):
            return "Miss!"

        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        deck = ship.get_deck(row, col)

        if deck is None:
            return "Miss!"

        if not deck.is_alive:
            return "Sunk!" if ship.is_drowned else "Hit!"

        ship.fire(row, col)
        return "Sunk!" if ship.is_drowned else "Hit!"

    def print_field(self) -> None:
        alive_symbol = "\u25A1"

        for row in range(self.size):
            line: list[str] = []
            for col in range(self.size):
                cell = (row, col)

                if cell not in self.field:
                    line.append("~")
                    continue

                ship = self.field[cell]
                deck = ship.get_deck(row, col)

                if deck is None:
                    line.append("?")
                    continue

                if deck.is_alive:
                    line.append(alive_symbol)
                else:
                    line.append("x" if ship.is_drowned else "*")

            print("\t".join(line))

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("Invalid number of ships: must be 10")

        size_counts: dict[int, int] = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in self.ships:
            ship_len = len(ship.decks)
            if ship_len not in size_counts:
                raise ValueError("Invalid ship size (allowed: 1..4)")
            size_counts[ship_len] += 1

        if size_counts != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise ValueError(
                f"Invalid fleet composition: "
                f"{size_counts} (expected {{1:4,2:3,3:2,4:1}})"
            )

        cell_to_ship_index: dict[tuple[int, int], int] = {}
        for ship_index, ship in enumerate(self.ships):
            for deck in ship.decks:
                cell = (deck.row, deck.column)
                cell_to_ship_index[cell] = ship_index

        for (row, col), ship_index in cell_to_ship_index.items():
            for d_row in (-1, 0, 1):
                for d_col in (-1, 0, 1):
                    if d_row == 0 and d_col == 0:
                        continue
                    neighbor = (row + d_row, col + d_col)
                    if neighbor in cell_to_ship_index:
                        other_ship_index = cell_to_ship_index[neighbor]
                        if other_ship_index != ship_index:
                            raise ValueError(
                                f"Ships are adjacent at "
                                f"{(row, col)} and {neighbor}"
                            )
