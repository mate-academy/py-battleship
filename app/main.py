from __future__ import annotations

from typing import Tuple, List


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
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        for row in range(start[0], end[0] + 1):
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, col))

    def get_deck(
            self,
            row: int,
            column: int
    ) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(
            self,
            row: int,
            column: int
    ) -> Ship | None:
        got_deck = self.get_deck(row, column)
        if got_deck and got_deck.is_alive:
            got_deck.is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True
            return self


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.field = {
            ship: Ship(*ship) for ship in ships
        }

    def fire(self, location: Tuple[int, int]) -> str:
        for ship_cord in self.field:
            ship = self.field[ship_cord].fire(*location)
            if ship:
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
