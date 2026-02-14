# flake8: noqa: *
import math

#u"\u25A1"
class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self):
        return f"{self.row}-{self.column}"


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        x = 1 if end[1] == start[1] else 0
        y = 1 if end[0] == start[0] else 0
        lenght = int(math.sqrt(((end[0] - start[0]) ** 2) + ((end[1] - start[1]) ** 2)))
        for i in range(lenght + 1):
            self.decks.append(Deck(start[0] + i * x, start[1] + i * y, True))

    def get_deck(self, row, column) -> None| Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
                if not any(deck.is_alive for deck in self.decks):
                    self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        self.ships = [Ship(ship[0], ship[1]) for ship in ships]

    def fire(self, place: tuple) -> str:
        for ship in self.ships:
            if ship.get_deck(place[0], place[1]) is not None:
                ship.fire(place[0], place[1])
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"
