from __future__ import annotations

from typing import List, Tuple, Dict


class Deck:

    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row: int = row
        self.column: int = column
        self.is_alive: bool = is_alive

    def hit(self) -> bool:
        self.is_alive = False
        return not self.is_alive


class Ship:

    def __init__(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        self.decks: List[Deck] = []
        self.is_drowned: bool = False

        start_row, start_col = start
        end_row, end_col = end

        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                self.decks.append(Deck(row, col))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck and deck.hit():
            self.is_drowned = all(not d.is_alive for d in self.decks)
            return "Sunk!" if self.is_drowned else "Hit!"
        return "Miss!"


class Battleship:

    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field: Dict[Tuple[int, int], Ship] = {}
        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        row, col = location
        if location in self.field:
            return self.field[location].fire(row, col)
        else:
            return "Miss!"
