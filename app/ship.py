from __future__ import annotations
from app.deck import Deck


class Coord:
    @staticmethod
    def verify_coord(data: tuple) -> None:
        if not isinstance(data, tuple):
            raise TypeError("Type should be 'tuple'")
        if len(data) != 2:
            raise ValueError("You should provide 2 integers inside")
        if len([i for i in data if type(i) == int]) != 2:
            raise ValueError("You should provide 2 integers inside")

    def __set_name__(self, owner: Ship, name: str) -> None:
        self.name = "_" + name

    def __get__(self, instance: Ship, owner: Ship) -> tuple:
        return instance.__dict__[self.name]

    def __set__(self, instance: Ship, value: tuple) -> None:
        self.verify_coord(value)
        instance.__dict__[self.name] = value


class Ship:
    start = Coord()
    end = Coord()

    def __init__(
        self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = self.create_decks(start, end)
        self.destroyed_decks = 0

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck if deck.is_alive else None

    def fire(self, row: int, column: int) -> None:
        target_deck = self.get_deck(row, column)
        if target_deck:
            target_deck.is_alive = False
            self.destroyed_decks += 1
        if self.destroyed_decks == len(self):
            self.is_drowned = True

    @staticmethod
    def create_decks(start: tuple, end: tuple) -> list:
        decks = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                decks.append(Deck(row, column))
        return decks

    def __len__(self) -> int:
        return len(self.decks)
