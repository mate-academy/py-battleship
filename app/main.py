from __future__ import annotations
from enum import Enum
from collections import Counter


class BattleshipError(Exception):
    pass


class ShipPositionError(BattleshipError):
    pass


class ShipTotalCountError(BattleshipError):
    pass


class ShipTypesCountError(BattleshipError):
    pass


class Tile(Enum):
    EMPTY = " ~ "


class Deck(Enum):
    ALIVE = " ■ "
    HIT = " □ "
    SUNK = " x "

    def next(self) -> Deck:
        states = (Deck.ALIVE, Deck.HIT, Deck.SUNK)
        current_index = states.index(self)
        next_index = min(current_index + 1, len(states) - 1)
        return states[next_index]


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.decks = self.create_decks()
        self.is_drowned = is_drowned

    def __len__(self) -> int:
        return len(self.decks)

    def create_decks(self) -> dict[tuple[int, int], Deck]:
        decks = {}

        if self.start[0] == self.end[0]:
            column = self.start[1]
            while column <= self.end[1]:
                decks[(self.start[0], column)] = Deck.ALIVE
                column += 1
        else:
            row = self.start[0]
            while row <= self.end[0]:
                decks[(row, self.start[1])] = Deck.ALIVE
                row += 1

        return decks

    def get_adjacent_cells(self) -> list[tuple[int, int]]:
        min_row, min_column = self.start
        max_row, max_column = self.end

        adjacent_cells = []
        for row in range(min_row - 1, max_row + 2):
            for column in range(min_column - 1, max_column + 2):
                if (row, column) not in self.decks:
                    if 0 <= row <= 9 and 0 <= column <= 9:
                        adjacent_cells.append((row, column))
        return adjacent_cells

    def get_deck(self, row: int, column: int) -> Deck:
        return self.decks[(row, column)]

    def fire(self, row: int, column: int) -> None:
        if not self.is_drowned:
            self.decks[(row, column)] = self.decks[(row, column)].next()
            if all(status == Deck.HIT for status in self.decks.values()):
                self.is_drowned = True
                for key in self.decks:
                    self.decks[key] = self.decks[key].next()


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], ...]],
            title_word: str | None = "РЕСПУБЛІКА"
    ) -> None:
        self.title_word = title_word
        self.fields = Battleship.create_fields(ships)
        self._validate_field()

    @staticmethod
    def create_fields(
            ships: list[tuple[tuple[int, int], ...]]
    ) -> dict[tuple, Ship]:
        fields = {}
        for ship in ships:
            ship_object = Ship(*ship)
            for cell in ship_object.decks:
                fields[cell] = ship_object
        return fields

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.fields:
            ship = self.fields[location]
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def column_coordinates_string(self) -> str:
        if self.title_word is None or len(self.title_word) != 10:
            return "   " + " ".join(str(i) + " " for i in range(10)) + "\n"
        return "   " + " ".join(char + " " for char in self.title_word) + "\n"

    def print_field(self) -> None:
        field_str = self.column_coordinates_string()

        for row in range(10):
            field_str += str(row) + " "
            for col in range(10):
                cell = (row, col)
                if cell in self.fields:
                    field_str += self.fields[cell].get_deck(*cell).value
                else:
                    field_str += Tile.EMPTY.value
            field_str += "\n"
        print(field_str)

    @staticmethod
    def _validate_ship_types(ships: set) -> None:
        ship_deck_counts = Counter(len(ship) for ship in ships)

        required_counts = {1: 4, 2: 3, 3: 2, 4: 1}

        for ship_size, required_count in required_counts.items():
            if ship_deck_counts.get(ship_size, 0) != required_count:
                raise ShipTypesCountError(
                    f"Field must have {required_count} {ship_size}-deck ships"
                )

    def _validate_ship_placement(self, ships: set) -> None:
        for ship in ships:
            ship_neighbours = ship.get_adjacent_cells()
            for cell in ship_neighbours:
                if cell in self.fields:
                    raise ShipPositionError(
                        f"Occupied cell {cell} "
                        f"too close to ship {ship}"
                    )

    def _validate_field(self) -> None:
        ships = set(self.fields.values())

        if len(ships) != 10:
            raise ShipTotalCountError("Field must have 10 ships")

        Battleship._validate_ship_types(ships)

        self._validate_ship_placement(ships)
