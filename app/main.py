from __future__ import annotations
from typing import List, Callable


class Deck:
    def __init__(
            self, row: int, column: int, is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:

        self.decks = []
        self.is_drowned = is_drowned
        for row in range(start[0], end[0] + 1):
            for col in range(start[1], end[1] + 1):
                deck = Deck(row, col)
                self.decks.append(deck)

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
                if all(not deck.is_alive for deck in self.decks):
                    self.is_drowned = True
                    return "Sunk!"
                return "Hit!"


class Battleship:
    def __init__(self, ships: List[Ship]) -> None:
        self.ships = ships
        self.field = {}
        self.neighbors = []

        for ship in self.ships:
            self.field[ship] = Ship(ship[0], ship[1])

    def validate_field(self) -> None:
        ships_count = []

        for ship in self.field.values():
            ships_count.append(len(ship.decks))
        sorted_ships = sorted(ships_count)

        if sorted_ships != [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]:
            print("Ships count or length is wrong")

        for ship in self.field.values():
            for deck in ship.decks:
                neighbors = [
                    (deck.row + i, deck.column + j)
                    for i in range(-1, 2)
                    for j in range(-1, 2)
                    if (i != 0 or j != 0)
                ]

                for neighbor_row, neighbor_col in neighbors:
                    for other_ship in self.field.values():
                        if other_ship != ship:
                            if any(
                                    (
                                        deck.row == neighbor_row
                                        and deck.column == neighbor_col
                                    )
                                    for deck in other_ship.decks
                            ):
                                print("Ships are located too close!")
                                return

        print("Ships are placed correctly!")

    def fire(self, location: tuple) -> Callable | str:
        for ship in self.field.values():
            if ship.get_deck(*location):
                return ship.fire(*location)
        return "Miss!"

    def print_field(self) -> list:
        field = []
        for i in range(0, 10):
            row = ["~ "] * 10
            field.append(row)

        for coordinates in self.ships:
            start_point, end_point = coordinates

            for row in range(start_point[0], end_point[0] + 1):
                for col in range(start_point[1], end_point[1] + 1):
                    field[row][col] = u"\u25A1 "

        for ship in self.field.values():
            if ship.is_drowned:
                for deck in ship.decks:
                    field[deck.row][deck.column] = u"\u2716 "

            if not ship.is_drowned:
                for deck in ship.decks:
                    if not deck.is_alive:
                        field[deck.row][deck.column] = "* "

        for row in field:
            print("".join(row))

        return field
