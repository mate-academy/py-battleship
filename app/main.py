from math import gcd
from typing import TypeAlias

from enum import Enum


class Symbol(Enum):
    WAVE = "~"
    SHIP = "□"
    HIT = "*"
    DROWNED = "x"


class Message(Enum):
    HIT = "Hit!"
    MISS = "Miss!"
    SUNK = "Sunk!"


BOARD_SIZE = 10

Coord: TypeAlias = tuple[int, int]
ShipDefinition: TypeAlias = tuple[Coord, Coord]


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return (
            f"({self.row}, {self.column}) is "
            f"{'alive' if self.is_alive else 'dead'}"
        )


class Ship:
    def __init__(
        self,
        start: Coord,
        end: Coord,
        is_drowned: bool = False,
    ) -> None:
        self.is_drowned = is_drowned
        self._create_deck(start, end)

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self._fire_deck(row, column)
        self._update_status()

    def _create_deck(
        self,
        start: Coord,
        end: Coord,
    ) -> None:
        # Create decks and save them to a list `self.decks`
        dx = end[0] - start[0]
        dy = end[1] - start[1]

        steps = gcd(abs(dx), abs(dy))

        if steps:
            self.decks = [
                Deck(start[0] + i * dx // steps, start[1] + i * dy // steps)
                for i in range(steps + 1)
            ]
        else:
            self.decks = [Deck(start[0], start[1])]

    def _fire_deck(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False

    def _update_status(self) -> None:
        for deck in self.decks:
            if deck.is_alive:
                return

        self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[ShipDefinition]) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.board = [
            [Symbol.WAVE for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)
        ]
        self.field: dict[Coord, Ship] = {}

        self.place_ships()

    def place_ships(self) -> None:
        for ship in self.ships:
            for deck in ship.decks:
                self.board[deck.row][deck.column] = Symbol.SHIP
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: Coord) -> str:
        ship = self.field.get(location)
        if ship:
            self._hit_deck(ship, location)
            if ship.is_drowned:
                self._sunk_ship(ship)
                return Message.SUNK.value
            return Message.HIT.value
        return Message.MISS.value

    def print_field(self) -> None:
        for row in self.board:
            for cell in row:
                print(cell.value, end=" ")
            print()

    def _paint_field(self, location: Coord, symbol: Symbol) -> None:
        self.board[location[0]][location[1]] = symbol

    def _sunk_ship(self, ship: Ship) -> None:
        for deck in ship.decks:
            self._paint_field((deck.row, deck.column), Symbol.DROWNED)

    def _hit_deck(self, ship: Ship, location: Coord) -> None:
        ship.fire(*location)
        self._paint_field(location, Symbol.HIT)
