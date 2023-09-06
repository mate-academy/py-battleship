from typing import Union


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
        self.start = start
        self.end = end
        self.decks = []
        self.is_drowned = is_drowned
        self.set_decks(start, end)

    def set_decks(self, start: tuple, end: tuple) -> None:
        if start == end:
            self.decks.append(Deck(start[0], start[1]))
        elif start[0] == end[0]:
            for i in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], i))
        elif start[1] == end[1]:
            for i in range(start[0], end[0] + 1):
                self.decks.append(Deck(i, start[1]))

    def get_deck(self, row: int, column: int) -> Union[Deck, None]:
        for ship_deck in self.decks:
            if (ship_deck.row, ship_deck.column) == (row, column):
                return ship_deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not ship_deck.is_alive for ship_deck in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            if ship.get_deck(*location):
                ship.fire(*location)
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
