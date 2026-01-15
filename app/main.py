from __future__ import annotations

from typing import List, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    @classmethod
    def create_decks(cls, start: tuple, end: tuple) -> List[Deck]:
        return [
            cls(row, column)
            for column in range(start[1], end[1] + 1)
            for row in range(start[0], end[0] + 1)
        ]


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.decks = Deck.create_decks(start, end)
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            self.is_drowned = all(not deck.is_alive for deck in self.decks)

    @classmethod
    def create_ships(cls, ships: list) -> list[Ship]:
        return [cls(*ship) for ship in ships]


class Battleship:

    def __init__(self, ships: list[tuple]) -> None:
        self.field = self._create_field(ships)

    @staticmethod
    def _create_field(ships: list[tuple]) -> dict:
        ships = Ship.create_ships(ships)
        fields = {}
        for ship in ships:
            for deck in ship.decks:
                fields[(deck.row, deck.column)] = ship
        return fields

    def fire(self, location: tuple) -> str:
        result = "Miss!"
        if location in self.field:
            result = "Hit!"
            ship = self.field[location]
            ship.fire(*location)
            if ship.is_drowned:
                result = "Sunk!"

        return result

    def print_field(self) -> None:

        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field[(row, column)]
                    if ship.is_drowned:
                        print("x", end=" ")
                    elif not ship.get_deck(row, column).is_alive:
                        print("*", end=" ")
                    else:
                        print(u"\u25A1", end=" ")
                else:
                    print("~", end=" ")
            else:
                print()
