from __future__ import annotations
from typing import Any


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        if self.start == self.end:
            self.decks.append(Deck(self.start[0], self.start[1]))

        length_vert = self.end[0] - self.start[0]
        length_horiz = self.end[1] - self.start[1]

        if length_vert >= 1:
            for deck in range(length_vert + 1):
                part = (self.start[0] + deck, self.start[1])
                self.decks.append(Deck(part[0], part[1]))

        if length_horiz >= 1:
            for deck in range(length_horiz + 1):
                part = (self.start[0], self.start[1] + deck)
                self.decks.append(Deck(part[0], part[1]))

    def get_deck(self, row: int, column: int) -> Any:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        alive = 0
        for part in self.decks:
            if part.is_alive:
                alive += 1
        if alive < 1:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}

        for ship in ships:
            if ship[0][0] > ship[1][0] or ship[0][1] > ship[1][1]:
                ship = (ship[1], ship[0])
            self.field[ship] = Ship(ship[0], ship[1])

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            for deck in ship.decks:
                if location[0] == deck.row and location[1] == deck.column:
                    ship.fire(location[0], location[1])
                    if ship.is_drowned:
                        return "Sunk!"
                    return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        matrix = []
        for _ in range(10):
            new_line = []
            for _ in range(10):
                new_line.append("~")
            matrix.append(new_line)

        for ship in self.field.values():
            for deck in ship.decks:
                if not ship.is_drowned:
                    if not deck.is_alive:
                        matrix[deck.row][deck.column] = "*"
                        continue
                    matrix[deck.row][deck.column] = "□"
                else:
                    matrix[deck.row][deck.column] = "x"

        for line in matrix:
            lines = ""
            for column in line:
                lines += f" {column} "
            print(lines)
