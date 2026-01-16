from typing import Optional, List, Tuple


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
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
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
            return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field: dict[Tuple[int, int], Ship] = {}
        for start, end in ships:
            instance = Ship(start, end)
            for deck in instance.decks:
                self.field[(deck.row, deck.column)] = instance

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            return ship.fire(*location)
        return "Miss!"
