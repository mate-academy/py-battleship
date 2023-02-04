from __future__ import annotations
from typing import Tuple, List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = []
        if start[0] == end[0]:
            self.decks = [
                Deck(start[0], i)
                for i in range(start[1], end[1] + 1)
            ]
        else:
            self.decks = [
                Deck(i, start[1])
                for i in range(start[0], end[0] + 1)
            ]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        fired_deck = self.get_deck(row, column)
        fired_deck.is_alive = False
        self.decks.remove(fired_deck)
        if not self.decks:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: List[Tuple]) -> None:
        self.field = {}
        for start, end in ships:
            ship = Ship(start, end)
            if start[0] == end[0]:
                self.field.update({
                    (start[0], i): ship
                    for i in range(start[1], end[1] + 1)
                })
            else:
                self.field.update({
                    (i, start[1]): ship
                    for i in range(start[0], end[0] + 1)
                })

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        self.field[location].fire(location[0], location[1])
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        field_symbols = []
        for row in range(10):
            for col in range(10):
                if (row, col) not in self.field:
                    field_symbols.append("~")
                elif self.field[(row, col)].is_drowned:
                    field_symbols.append("x")
                elif self.field[(row, col)].get_deck(row, col) is None:
                    field_symbols.append("*")
                else:
                    field_symbols.append(u"\u25A1")
        num = 0
        while num < 100:
            print("  ".join(field_symbols[num:num + 10]))
            num += 10
