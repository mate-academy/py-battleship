from typing import List


class EmptyField:
    @staticmethod
    def fire(*args) -> str:
        return "Miss!"


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.ship_len = end[0] - start[0] + end[1] - start[1] + 1
        dx = 1 if end[0] - start[0] else 0
        dy = 1 if end[1] - start[1] else 0
        self.deck = {}
        for i in range(self.ship_len):
            x_ = start[0] + dx * i
            y_ = start[1] + dy * i
            self.deck[(x_, y_)] = Deck(x_, y_)

    def get_deck(self, row: int, column: int) -> Deck:
        return self.deck[(row, column)]

    def fire(self, row: int, column: int) -> str:
        self.get_deck(row, column).is_alive = False
        if any([deck.is_alive for deck in self.deck.values()]):
            return "Hit!"
        self.is_drowned = True
        return "Sunk!"


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.field = [[EmptyField for _ in range(10)] for _ in range(10)]
        for ship in ships:
            ship = Ship(ship[0], ship[1])
            for coordinate in ship.deck.keys():
                self.field[coordinate[0]][coordinate[1]] = ship

    def fire(self, location: tuple) -> str:
        return self.field[location[0]][location[1]].fire(
            location[0], location[1]
        )
