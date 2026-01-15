from typing import Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        if self.start[0] == self.end[0]:
            for i in range(min(self.start[1], self.end[1]),
                           max(self.start[1], self.end[1]) + 1):
                self.decks.append(Deck(self.start[0], i))
        elif self.start[1] == self.end[1]:
            for i in range(min(self.start[0], self.end[0]),
                           max(self.start[0], self.end[0]) + 1):
                self.decks.append(Deck(i, self.start[1]))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck is None:
            return "Miss!"
        else:
            deck.is_alive = False
            if all(deck.is_alive is False for deck in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = []
        self.field = {}
        for ship in ships:
            reference = Ship(ship[0], ship[1])
            self.ships.append(reference)
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            return ship.fire(*location)
        return "Miss!"
