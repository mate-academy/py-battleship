from __future__ import annotations
from typing import Any


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __str__(self) -> str:
        return (
            f"Deck(row={self.row}, "
            f"column={self.column}, "
            f"is_alive={self.is_alive})"
        )


class Ship:
    def __init__(self, start: Deck, end: Deck,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

    def ships_create(self) -> Any:
        if (self.start.row == self.end.row
                and self.start.column == self.end.column):
            self.decks.append(Deck(self.start.row, self.start.column, True))
        else:
            if self.start.row == self.end.row:
                start_col = self.start.column
                end_col = self.end.column
                self.decks.extend(
                    [Deck(self.start.row, col, True)
                     for col in range(start_col, end_col + 1)]
                )
            elif self.start.column == self.end.column:
                start_row = self.start.row
                end_row = self.end.row
                self.decks.extend(
                    [Deck(row, self.start.column, True)
                     for row in range(start_row, end_row + 1)]
                )

        return self

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck is not None:
            deck.is_alive = False
            for deck in self.decks:
                if deck.is_alive:
                    return False
            self.is_drowned = True
            return True
        return False


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = {}
        for ship in self.ships:
            self.field[ship] = Ship(
                Deck(ship[0][0], ship[0][1]),
                Deck(ship[1][0], ship[1][1])
            ).ships_create()

    def fire(self, location: tuple) -> str:
        for ship in self.field:
            deck = self.field[ship].get_deck(location[0], location[1])
            if deck is not None and deck.is_alive:
                if self.field[ship].fire(location[0], location[1]):
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
