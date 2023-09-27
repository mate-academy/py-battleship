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
        self.field: List[List[Union[Deck, None, Ship]]] = \
            [[None for _ in range(10)] for _ in range(10)]

        for ship in self.ships:
            for coordinates in ship.decks:
                self.field[coordinates[0]][coordinates[1]] = ship

        self._validate_field()

    def _validate_field(self) -> bool:
        total_ship = 0
        single_ship = 0
        double_ship = 0
        three_ship = 0
        four_ship = 0

        for ship in self.ships:
            total_ship += 1
            deck_count = len(ship.decks)
            if deck_count == 1:
                single_ship += 1
            elif deck_count == 2:
                double_ship += 1
            elif deck_count == 3:
                three_ship += 1
            elif deck_count == 4:
                four_ship += 1

        if total_ship != 10:
            print("The total number of ships does not correspond to 10")
            return False
        if single_ship != 4:
            print("The number of single-deck ships is incorrect")
            return False
        if double_ship != 3:
            print("The number of double-deck ships is incorrect")
            return False
        if three_ship != 2:
            print("The number of three-deck ships is incorrect")
            return False
        if four_ship != 1:
            print("The number of four-deck ships is incorrect")
            return False

        for ship in self.ships:
            for deck in ship.decks:
                for row in range(max(0, deck[0] - 1),
                                 min(deck[0] + 2, len(self.field))):
                    for cel in range(max(0, deck[1] - 1),
                                     min(deck[1] + 2, len(self.field[0]))):
                        if (row != deck[0] or cel != deck[1]) \
                                and self.field[row][cel] is not None:
                            print("The ships are located nearby!")
                            return False

        print("Ships are placed correctly!")
        return True

    def fire(self, location: Tuple[int, int]) -> str:
        row, col = location
        if self.field[row][col] is not None:
            ship = self.field[row][col]
            hit = ship.fire(row, col)
            if hit:
                if ship.is_drowned:
                    return "Sunk!"
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
