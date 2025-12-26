from typing import List


class ShipsQuantityError(Exception):
    """Error that handles possible quantity of ships"""


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return "x"

    def __str__(self) -> str:
        if self.is_alive:
            return "□"
        return "*"


class Ship:
    def __init__(self, start: int, end: int, is_drowned: bool = False) -> None:
        self.start_row, self.start_column = start
        self.end_row, self.end_column = end
        self.is_drowned = is_drowned
        self.decks = []
        if self.end_row - self.start_row > 0:
            for row_cell in range(self.start_row, self.end_row + 1):
                self.decks.append(Deck(row_cell, self.start_column))
        else:
            for column_cell in range(self.start_column, self.end_column + 1):
                self.decks.append(Deck(self.start_row, column_cell))

    def get_deck(self, row: int, column: int) -> tuple | None:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return row, column

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                deck.is_alive = False
                break
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    FIELD_SIZE = 10

    def __init__(self, ships: List[tuple]) -> None:
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}
        self._validate_input()

    def fire(self, location: tuple) -> str:
        for ship in self.field.values():
            deck = ship.get_deck(location[0], location[1])
            if deck:
                ship.fire(deck[0], deck[1])
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def _validate_input(self) -> None:
        if len(self.field) != 10:
            raise ShipsQuantityError(f"Total amount of ships must be 10, "
                                     f"not {len(self.field)}")
        decks = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }
        limitations = {
            1: 4,
            2: 3,
            3: 2,
            4: 1
        }
        for ship in self.field.values():
            decks[len(ship.decks)] += 1
        for ship, quantity in decks.items():
            if limitations[ship] != quantity:
                raise ShipsQuantityError(f"There should be {limitations[ship]}"
                                         f" {ship}-deck ships, not {quantity}")

    def print_field(self) -> None:
        field = [
            ["~" for _ in range(Battleship.FIELD_SIZE)]
            for _ in range(Battleship.FIELD_SIZE)
        ]
        for ship in self.field.values():
            for deck in ship.decks:
                if ship.is_drowned:
                    field[deck.row][deck.column] = repr(deck)
                else:
                    field[deck.row][deck.column] = str(deck)
        for row in field:
            print(*row)
