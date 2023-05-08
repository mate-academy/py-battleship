from typing import Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        for coord_row in range(start[0], end[0] + 1):
            if start[0] == end[0]:
                columns = range(start[1], end[1] + 1)
            else:
                columns = [start[1]]
            for column in columns:
                self.decks.append(Deck(coord_row, column))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is not None:
            deck.is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for coords in ships:
            start, end = coords[0], coords[1]
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)

            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
