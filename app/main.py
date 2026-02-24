from __future__ import annotations
from typing import Dict, List, Optional, Tuple


Coord = Tuple[int, int]


class Deck:
    def __init__(
            self, row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    @property
    def coord(self) -> Coord:
        return (self.row, self.column)


class Ship:
    def __init__(self,
                 start: Coord,
                 end: Coord,
                 is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self._create_decks()

    def _create_decks(self) -> List[Deck]:
        (start_row, start_column), (
            end_row,
            end_column,
        ) = self.start, self.end

        if start_row != end_row and start_column != end_column:
            raise ValueError("Ship must be horizontal or vertical.")

        row_start, row_end = sorted((start_row, end_row))
        column_start, column_end = sorted(
            (start_column, end_column)
        )

        decks: List[Deck] = []

        if row_start == row_end:
            for column_index in range(
                    column_start, column_end + 1
            ):
                decks.append(Deck(row_start, column_index))
        else:
            for row_index in range(
                    row_start, row_end + 1
            ):
                decks.append(Deck(row_index, column_start))

        return decks

    def get_deck(
            self,
            row: int,
            column: int,
    ) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is None:
            return
        deck.is_alive = False
        self.is_drowned = all(not d.is_alive for d in self.decks)


class Battleship:
    SIZE : int = 10

    def __init__(self, ships: List[Tuple[Coord, Coord]]) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field: Dict[Coord, Ship] = {}
        self._index_field()

    def _index_field(self) -> None:
        for ship in self.ships:
            for deck in ship.decks:
                self._validade_coord(deck.coord)
                if deck.coord in self.field:
                    raise ValueError("Overlapping ships detected.")
                self.field[deck.coord] = ship

    def _validade_coord(self, coord: Coord) -> None:
        row, column = coord
        if not (0 <= row < self.SIZE and 0 <= column < self.SIZE):
            raise ValueError(f"Coordinate out of bounds: {coord}.")

    def fire(self, location: tuple) -> str:
        if not isinstance(location, tuple) or len(location) != 2:
            raise TypeError("Location must be a tuple (row, column).")

        row, column = location
        if not isinstance(row, int) or not isinstance(column, int):
            raise TypeError("Row and column must be integers.")

        self._validade_coord((row, column))

        ship = self.field.get((row, column))
        if ship is None:
            return "Miss!"

        ship.fire(row, column)
        return "Sunk!" if ship.is_drowned else "Hit!"
