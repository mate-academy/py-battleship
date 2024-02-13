from typing import List, Tuple


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
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
        self.decks = [
            Deck(i, j)
            for i in range(start[0], end[0] + 1)
            for j in range(start[1], end[1] + 1)
        ]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True
                return "Sunk!"
            else:
                return "Hit!"
        else:
            return "Miss!"


class Battleship:
    def __init__(
        self,
        ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field = {}
        for ship_coords in ships:
            ship = Ship(*ship_coords)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        ship = self.field.get(location)
        if ship:
            return ship.fire(*location)
        else:
            return "Miss!"
