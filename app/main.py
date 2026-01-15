from typing import Any


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: int, end: int, is_drowned: bool = False) -> None:
        self.desks = []
        start_row, start_col = start
        end_row, end_col = end
        if start_row == end_row:
            for col in range(start_col, end_col + 1):
                self.desks.append(Deck(start_row, col))
        elif start_col == end_col:
            for row in range(start_row, end_row + 1):
                self.desks.append(Deck(row, start_col))
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Any:
        for desk in self.desks:
            if desk.row == row and desk.column == column:
                return desk
        return None

    def fire(self, row: int, column: int) -> None:
        desk = self.get_deck(row, column)
        if desk:
            desk.is_alive = False
            self.check_drowned()

    def check_drowned(self) -> None:
        if all(not deck.is_alive for deck in self.desks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for ship in ships:
            start, end = ship
            new_ship = Ship(start, end)
            for deck in new_ship.desks:
                self.field[(deck.row, deck.column)] = new_ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.get_deck(location[0], location[1])
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        rows = [["~"] * 10 for _ in range(10)]
        for location, ship in self.field.items():
            row = location[0]
            col = location[1]
            if ship.is_drowned:
                rows[row][col] = "x"
            elif not ship.get_deck(*location).is_alive:
                rows[row][col] = "*"
            else:
                rows[row][col] = u"\u25A1"
        joined_rows = ["    ".join(row) for row in rows]
        field = "\n".join(joined_rows)
        print(field)
