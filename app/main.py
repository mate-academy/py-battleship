from __future__ import annotations
from typing import List, Tuple


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
        self.decks = []
        self.is_drowned = is_drowned

        if start[0] == end[0]:
            row = start[0]
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, col))
        elif start[1] == end[1]:
            col = start[1]
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, col))

    def get_deck(
            self,
            row: int,
            column: int
    ) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(
            self,
            row: int,
            column: int
    ) -> str:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = [["~" for _ in range(10)] for _ in range(10)]

        for ship in self.ships:
            for deck in ship.decks:
                self.field[deck.row][deck.column] = "□"

    def fire(
            self,
            location: tuple
    ) -> str:
        row, col = location
        for ship in self.ships:
            result = ship.fire(row, col)
            if result != "Miss!":
                self.field[row][col] = "*" if result == "Hit!" else "x"
                return result
        self.field[row][col] = "~"
        return "Miss!"

    def print_field(self) -> None:
        for row in self.field:
            print(" ".join(row))
