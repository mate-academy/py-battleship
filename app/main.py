from typing import List, Tuple, Union
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


def test_battleship() -> None:
    battle_ship = Battleship(
        ships=[
            ((2, 0), (2, 3)),
            ((4, 5), (4, 6)),
            ((3, 8), (3, 9)),
            ((6, 0), (8, 0)),
            ((6, 4), (6, 6)),
            ((6, 8), (6, 9)),
            ((9, 9), (9, 9)),
            ((9, 5), (9, 5)),
            ((9, 3), (9, 3)),
            ((9, 7), (9, 7)),
        ]
    )

    field: List[List[Union[Deck, None, Ship]]] = \
        [[None for _ in range(10)] for _ in range(10)]

    for ship in battle_ship.ships:
        for deck in ship.decks:
            field[deck[0]][deck[1]] = ship

    for row in range(10):
        for col in range(10):
            if field[row][col] is None:
                field[row][col] = Deck(row, col)

    battle_ship.print_field(field)
