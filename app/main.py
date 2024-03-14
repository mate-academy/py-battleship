from typing import Tuple, List, Optional


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
        self.decks: List[Deck] = []
        self.is_drowned = is_drowned
        horizontal = start[0] == end[0]
        row_range = (range(start[0], end[0] + 1)
                     if not horizontal else [start[0]])
        col_range = range(start[1], end[1] + 1) if horizontal else [start[1]]

        for row in row_range:
            for column in col_range:
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.board = [["~" for _ in range(10)] for _ in range(10)]
        self.ships = []
        self._place_ships(ships)

    def _place_ships(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        for ship_coords in ships:
            ship = Ship(*ship_coords)
            self.ships.append(ship)
            for deck in ship.decks:
                self.board[deck.row][deck.column] = "□"

    def fire(self, ceil: Tuple[int, int]) -> str:
        row, column = ceil
        for ship in self.ships:
            result = ship.fire(row, column)
            if result in ["Hit!", "Sunk!"]:
                self.board[row][column] = "*" if result == "Hit!" else "x"
                return result
        self.board[row][column] = "X"
        return "Miss!"

    def print_field(self) -> None:
        symbol_map = {"~": "~", "□": u"\u25A1", "X": "X", "*": "*", "x": "x"}
        for row in self.board:
            print(" ".join(symbol_map[cell] for cell in row))
