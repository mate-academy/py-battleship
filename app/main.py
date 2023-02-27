from __future__ import annotations

from typing import Any, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: Deck, end: Deck,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

    def create_ship(self) -> Any:
        for row in range(self.start.row, self.end.row + 1):
            for column in range(self.start.column, self.end.column + 1):
                self.decks.append(Deck(row, column))
        return self

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> bool:
        self.get_deck(row, column).is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True
            return True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship in ships:
            self.field[ship] = Ship(
                Deck(ship[0][0], ship[0][1]),
                Deck(ship[1][0], ship[1][1])
            ).create_ship()

    def fire(self, location: tuple) -> str:
        for ship in self.field:
            if self.field[ship].get_deck(location[0], location[1]):
                if self.field[ship].fire(location[0], location[1]):
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
