from typing import List, Optional


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
        self.decks = [Deck(row, column)
                      for row, column in self.get_coordinates(start, end)]
        self.is_drowned = is_drowned

    @staticmethod
    def get_coordinates(start: tuple, end: tuple) -> List[tuple]:
        coordinates = []
        if start[0] == end[0]:
            coordinates = [(start[0], column)
                           for column in range(start[1], end[1] + 1)]
        elif start[1] == end[1]:
            coordinates = [(row, start[1])
                           for row in range(start[0], end[0] + 1)]
        return coordinates

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.field = {}
        for ship in ships:
            ship_obj = Ship(ship[0], ship[1])
            for coordinate in ship_obj.decks:
                self.field[coordinate.row, coordinate.column] = ship_obj

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        else:
            return "Miss!"
