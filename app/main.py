from colorama import Fore, Style, init
from typing import List
init()


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
        self.game_field = self.create_battle_dict(ships)
        self.create_field = self.print_field()

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)
            return "Sunk!" if ship.is_drowned else "Hit!"

    def create_battle_dict(self, ships: List[tuple]) -> None:
        for start, end in ships:
            boat = Ship(start, end)
            for cord_x in range(start[0], end[0] + 1):
                for cord_y in range(start[1], end[1] + 1):
                    if (cord_x, cord_y) not in self.field:
                        self.field[(cord_x, cord_y)] = boat

    def print_field(self) -> str:
        create_field = [["~" for _ in range(10)] for _ in range(10)]
        for start, end in self.ships:
            for cord_x in range(start[0], end[0] + 1):
                for cord_y in range(start[1], end[1] + 1):
                    create_field[cord_x][cord_y] = u"\u25A1"
        for (row, col), ship in self.field.items():
            if ship.is_drowned:
                create_field[row][col] = Fore.RED + "X" + Style.RESET_ALL
            else:
                create_field[row][col] = Fore.GREEN + "*" + Style.RESET_ALL

        return "\n".join(" ".join(row) for row in create_field)
