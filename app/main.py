from __future__ import annotations


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
            start: tuple[int],
            end: tuple[int],
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        self._create_ship(start, end)

    def _create_ship(self, start: tuple[int], end: tuple[int]) -> None:
        col_coord, row_coord = (start[0], end[0]), (start[1], end[1])
        rows_range = range(min(col_coord), max(col_coord) + 1)
        col_range = range(min(row_coord), max(row_coord) + 1)

        for row in rows_range:
            for column in col_range:
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            alive_decks = [deck for deck in self.decks if deck.is_alive]
            if not alive_decks:
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship_start, ship_end in ships:
            ship = Ship(ship_start, ship_end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_fields(ships)

    def _validate_fields(self, ships: list[tuple]) -> None:
        ships_count = {1: 0, 2: 0, 3: 0, 4: 0}

        for ship_start, ship_end in ships:
            ship_len = max(
                abs(ship_start[0] - ship_end[0]),
                abs(ship_start[1] - ship_end[1])
            ) + 1
            ships_count[ship_len] += 1

        if ships_count != {1: 4, 2: 3, 3: 2, 4: 1} or len(ships) != 10:
            raise ValueError("Invalid ship configuration")

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        ship.fire(location[0], location[1])

        if ship.is_drowned:
            return "Sunk!"

        return "Hit!"

    def print_field(self) -> None:
        for row in range(10):
            for column in range(10):
                location = (row, column)
                if location not in self.field:
                    print("~", end=" ")
                else:
                    ship = self.field[location]
                    deck = ship.get_deck(row, column)
                    if not deck.is_alive:
                        print("x", end=" ")
                    else:
                        print(u"\u25A1", end=" ")
        print()
