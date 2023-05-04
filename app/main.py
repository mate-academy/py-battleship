from __future__ import annotations


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
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]

    def get_deck(
            self,
            row: int,
            column: int
    ) -> Deck:
        return next(
            deck
            for deck in self.decks
            if deck.row == row and deck.column == column
        )

    def fire(
            self,
            row: int,
            column: int
    ) -> bool:
        self.get_deck(row, column).is_alive = False

        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True

        return self.is_drowned


class Battleship:
    def __init__(
            self,
            ships: list
    ) -> None:
        self.ships = [Ship(ship[0], ship[1]) for ship in ships]
        self.field = {
            (deck.row, deck.column): ship
            for ship in self.ships
            for deck in ship.decks
        }

    def fire(
            self,
            location: tuple
    ) -> str:
        if location not in self.field:
            return "Miss!"

        self.field[location].fire(*location)

        return "Hit!" if not self.field[location].is_drowned else "Sunk!"
