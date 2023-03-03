from __future__ import annotations


class Deck:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.is_alive = True


class Ship:
    def __init__(self, start: tuple, end: tuple) -> None:
        self.start = start
        self.end = end
        self.is_drowned = False
        self.decks = []

    def create_deck(self) -> None:
        if self.start[0] == self.end[0]:
            for i in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], i))
        else:
            for i in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(i, self.start[1]))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        fired_deck = self.get_deck(row, column)
        if fired_deck:
            fired_deck.is_alive = False
        self.is_drowned = not any([deck.is_alive for deck in self.decks])


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}
        for value in self.field.values():
            value.create_deck()

    def fire(self, location: tuple) -> str:
        for key, value in self.field.items():
            if (location[0] in range(key[0][0], key[1][0] + 1)
                    and location[1] in range(key[0][1], key[1][1] + 1)):
                value.fire(location[0], location[1])
                if value.is_drowned is True:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
