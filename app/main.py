from collections.abc import Generator
from itertools import zip_longest
from typing import Any
from dataclasses import dataclass


@dataclass
class Deck:
    row: int
    column: int
    is_alive: bool = True


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
        self.decks: list[Deck] = [
            Deck(i, j) for i, j in Battleship.generate_coordinates(start, end)
        ]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck: Deck | None = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if not any(deck.is_alive for deck in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(
        self, ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field: dict[tuple[int, int], Ship] = {}

        for start, end in ships:
            ship: Ship = Ship(start, end)
            for coord in Battleship.generate_coordinates(start, end):
                self.field[coord] = ship

    def fire(self, location: tuple[int, int]) -> str:
        if (ship := self.field.get(location, None)) is not None:
            ship.fire(*location)
            return "Sunk!" if ship.is_drowned else "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        result: list[str] = []
        row: list[str] = []
        for row_coord in range(10):
            for col_coord in range(10):
                if ship := self.field.get((col_coord, row_coord)):
                    if ship.is_drowned:
                        row.append("x")
                    else:
                        deck: Deck | None = ship.get_deck(col_coord, row_coord)
                        row.append("\u25A1" if deck and deck.is_alive else "*")
                else:
                    row.append("~")
            result.append(" ".join(row))
            row = []
        print("\n".join(result))

    @staticmethod
    def generate_coordinates(
        start: tuple[int, int], end: tuple[int, int]
    ) -> Generator[tuple[int, int], Any, Any]:
        yield start
        coord: list[int] = [*start]
        for dx, dy in zip_longest(
            [1] * abs(end[0] - start[0]),
            [1] * abs(end[1] - start[1]),
            fillvalue=0,
        ):
            coord[0] += dx
            coord[1] += dy
            yield tuple(coord)  # type: ignore
