from typing import Tuple, List, Optional


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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, column)
            for column in range(start[1], end[1] + 1)
            for row in range(start[0], end[0] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
                return True
        return False


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.field = {}
        for ship in ships:
            self.ship = Ship(*ship)
            for deck in self.ship.decks:
                self.field[deck.row, deck.column] = self.ship

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            if ship.fire(location[0], location[1]):
                return "Sunk!"
            return "Hit!"
        return "Miss!"
