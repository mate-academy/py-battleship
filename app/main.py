from typing import List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) \
            -> None:
        self.is_drowned = is_drowned
        self.decks = []
        in_row = end[0] - start[0] + 1
        in_column = end[1] - start[1] + 1
        for row in range(in_row):
            for column in range(in_column):
                self.decks.append(Deck(start[0] + row, start[1] + column))

    def get_deck(self, row: int, column: int) -> Deck:
        return next(deck for deck in self.decks
                    if deck.row == row and deck.column == column)

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.field = {}
        for i in range(len(ships)):
            ship = Ship(ships[i][0], ships[i][1])
            for le in range(len(ship.decks)):
                self.field[(ship.decks[le].row, ship.decks[le].column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field.keys():
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
