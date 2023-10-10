from typing import Tuple, List


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        (start_row, start_column), (end_row, end_column) = start, end
        for row in range(start_row, end_row + 1):
            for column in range(start_column, end_column + 1):
                deck = Deck(row, column)
                self.decks.append(deck)

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is not None:
            deck.is_alive = False
            self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field = {}
        for ship in ships:
            current_ship = Ship(*ship)
            for deck in current_ship.decks:
                self.field.update({(deck.row, deck.column): current_ship})

    def fire(self, location: Tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"
        current_ship = self.field[location]
        current_ship.fire(*location)
        if current_ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        field = [["~"] * 10 for x in range(10)]
        for row in range(10):
            for column in range(10):
                location = (row, column)
                if location in self.field:
                    current_ship = self.field[location]
                    deck = current_ship.get_deck(row, column)
                    if deck.is_alive:
                        field[row][column] = "□"
                    elif not deck.is_alive and not current_ship.is_drowned:
                        field[row][column] = "*"
                    elif not deck.is_alive and current_ship.is_drowned:
                        field[row][column] = "X"

        for row in field:
            print("    ".join(row))
