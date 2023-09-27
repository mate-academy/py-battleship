from typing import List, Tuple
from app.Ship import Ship


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Battleship:
    def __init__(self, ships: List[Tuple]) -> None:
        self.ships = [Ship(*ship_coordinates) for ship_coordinates in ships]
        self.field = {}

        for ship in self.ships:
            for coordinates in ship.decks:
                self.field[coordinates] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            hit = ship.fire(*location)
            if hit:
                if ship.is_drowned:
                    return "Sunk!"
                else:
                    return "Hit!"
        return "Miss!"

    def print_field(self, field: list) -> None:
        for row in field:
            for column in row:
                if isinstance(column, Deck):
                    if column.is_alive:
                        print(u"\u25A1", end="")
                    else:
                        print("*", end="")
                elif isinstance(column, Ship):
                    if column.is_drowned:
                        print("x", end="")
                    else:
                        print(u"\u25A1", end="")
                else:
                    print("~", end="")
            print()
