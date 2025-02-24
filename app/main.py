from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Deck:
    row: int
    column: int
    is_alive: bool = True
    symbol: str = "□"


@dataclass
class Ship:
    start: Tuple[int, int]
    end: Tuple[int, int]
    decks: List[Deck] = None
    is_drowned: bool = False

    def __post_init__(self) -> None:
        if self.decks is None:
            self.decks = []
        if self.start[0] == self.end[0]:
            for col in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], col))
        elif self.start[1] == self.end[1]:
            for row in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(row, self.start[1]))
        else:
            raise ValueError("Invalid ship coordinates. "
                             "Ship must be horizontal or vertical.")

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            deck.symbol = "x"
            if self.is_ship_sunk():
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def is_ship_sunk(self) -> bool:
        return all(not deck.is_alive for deck in self.decks)


@dataclass
class Battleship:
    ships: List[Ship]
    field: List[List[str]] = None

    def __post_init__(self) -> None:
        self.field = [["~" for _ in range(10)] for _ in range(10)]
        self.ships = [Ship(start, end) for start, end in self.ships]
        self._validate_field()

        for ship in self.ships:
            for deck in ship.decks:
                self.field[deck.row][deck.column] = deck.symbol

    def fire(self, location: Tuple[int, int]) -> str:
        row, column = location

        if 0 <= row < 10 and 0 <= column < 10:
            hit_result = "Miss!"
            for ship in self.ships:
                hit_result = ship.fire(row, column)
                if hit_result != "Miss!":
                    self.field[row][column] = "x"
                    break
            else:
                self.field[row][column] = "O"

            return hit_result
        return "Invalid coordinates!"

    def print_field(self) -> None:
        for row in self.field:
            print(" ".join(row))

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("There must be exactly 10 ships.")

        single_deck_ships = sum(
            1 for ship in self.ships if len(ship.decks) == 1
        )
        double_deck_ships = sum(
            1 for ship in self.ships if len(ship.decks) == 2
        )
        three_deck_ships = sum(
            1 for ship in self.ships if len(ship.decks) == 3
        )
        four_deck_ships = sum(
            1 for ship in self.ships if len(ship.decks) == 4
        )

        if not (
                single_deck_ships == 4
                and double_deck_ships == 3
                and three_deck_ships == 2
                and four_deck_ships == 1
        ):
            raise ValueError("Ships count is not correct: 4 single-deck,"
                             " 3 double-deck, 2 three-deck, and 1 four-deck.")

        for coord_x in range(10):
            for coord_y in range(10):
                if (self.field[coord_x][coord_y] == "□"
                        and self._is_adjacent(coord_x, coord_y)):
                    raise ValueError("Ships are located in adjacent "
                                     "cells, even diagonally.")

    def _is_adjacent(self, row: int, column: int) -> bool:
        directions: List[Tuple[int, int]] = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1)
        ]

        return any(
            0 <= row + dr < 10 and 0 <= column + dc < 10
            and self.field[row + dr][column + dc] == "□"
            for dr, dc in directions
        )
