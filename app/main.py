from typing import List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
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
        self.decks = []
        if start == end:
            self.decks.append(Deck(*start))
        elif end[0] == start[0] and end[1] != start[1]:
            columns = range(start[1], end[1] + 1)
            for column in columns:
                self.decks.append(Deck(start[0], column))
        else:
            rows = range(start[0], end[0] + 1)
            for row in rows:
                self.decks.append(Deck(row, start[1]))
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.field = {}
        for coordinates in ships:
            start, end = coordinates[0], coordinates[1]
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field.update({(deck.row, deck.column): ship})

    def fire(self, location: tuple) -> str:
        if location in self.field.keys():
            ship = self.field[location]
            ship.fire(*location)
            if all(not deck.is_alive for deck in ship.decks):
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            line = ""
            for column in range(10):
                ship = self.field.get((row, column))
                if ship is not None:
                    if ship.is_drowned:
                        line += "x    "
                    else:
                        deck = ship.get_deck(row, column)
                        if deck.is_alive:
                            line += u"\u25A1    "
                        else:
                            line += "*    "
                else:
                    line += "~    "
            print(f"{line}\n")
