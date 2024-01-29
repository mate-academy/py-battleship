from __future__ import annotations


class Deck:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.is_alive = True


class Ship:
    def __init__(self, start: tuple, end: tuple) -> None:
        self.decks = [
            Deck(row, column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]
        self.is_drowned = False

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck if deck.is_alive else None

    def get_alive_decks_count(self) -> int:
        return sum(1 for deck in self.decks if deck.is_alive)

    def fire(self, row: int, column: int) -> str:
        if deck := self.get_deck(row, column):
            deck.is_alive = False
            if self.get_alive_decks_count():
                return "Hit!"
            self.is_drowned = True
            return "Sunk!"


class Battleship:
    def __init__(self, ships: list) -> None:
        ships_instances = [Ship(ship[0], ship[1]) for ship in ships]
        self.field = {
            (deck.row, deck.column): ship
            for ship in ships_instances
            for deck in ship.decks
        }

    def fire(self, location: tuple) -> str:
        if ship := self.field.get(location):
            return ship.fire(*location)
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            field_row = ""
            for column in range(10):
                if ship := self.field.get((row, column)):
                    if ship.get_deck(row, column):
                        field_row += u"\u25A1\t"
                        continue
                    field_row += "x\t"
                else:
                    field_row += "~\t"
            print(field_row)
