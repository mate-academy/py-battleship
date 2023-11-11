from typing import List, Tuple


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
        self.is_drowned = is_drowned
        self.decks = [Deck(row, column) for row in range(start[0], end[0] + 1)
                      for column in range(start[1], end[1] + 1)]

    def get_deck(
            self,
            row: int,
            column: int
    ) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        if not self.is_drowned:
            deck = self.get_deck(row, column)
            if deck:
                deck.is_alive = False
                if all(not current_deck.is_alive
                       for current_deck in self.decks):
                    self.is_drowned = True
        if self.is_drowned:
            for deck in self.decks:
                deck.is_alive = False
            return "Sunk!"
        return "Hit!"


class Battleship:
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field = {}
        for start, end in ships:
            ship = Ship(start, end)
            for row in range(start[0], end[0] + 1):
                for column in range(start[1], end[1] + 1):
                    self.field[(row, column)] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            result = ship.fire(location[0], location[1])
            if ship.is_drowned:
                del self.field[location]
            return result
        return "Miss!"
