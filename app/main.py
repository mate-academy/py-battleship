from typing import List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self, start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:

        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.deck = []

        self.create_ship()

    def create_ship(self) -> None:
        for coord_x in range(
                self.start[0], self.end[0] + 1
        ):

            for coord_y in range(self.start[1], self.end[1] + 1):
                if coord_x == self.start[0] or coord_y == self.start[1]:
                    self.deck.append(Deck(coord_x, coord_y))

    def get_deck(self, row: tuple, column: tuple) -> tuple:
        for deck in self.deck:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: tuple, column: tuple) -> None:
        deck = self.get_deck(row, column)
        if deck is not None:
            deck.is_alive = False
            if all(not d.is_alive for d in self.deck):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.ships = ships
        self.field = {}
        self.game_field = self.create_battle_field(ships)
        self.placement_of_ships()

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)
            return "Sunk!" if ship.is_drowned else "Hit!"

    def create_battle_field(self, ships: List[tuple]) -> List[list[str]]:
        return [["~" for _ in range(10)] for _ in range(10)]

    def placement_of_ships(self) -> None:
        square = "\u25A1"
        for ship in self.ships:

            boat = Ship(*ship)
            (row1, column1), (row2, column2) = ship
            if row1 == row2:
                for column in range(column1, column2 + 1):
                    self.game_field[row1][column] = square
                    self.field[(row1, column)] = boat
            else:
                for row1 in range(row1, row2 + 1):
                    self.game_field[row1][column1] = square
                    self.field[(row1, column1)] = boat
