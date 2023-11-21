import dataclasses
from typing import Optional


@dataclasses.dataclass
class Deck:
    row: int
    column: int
    is_alive: bool = True


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.decks = None
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.fill_decs()

    def fill_decs(self) -> None:
        if self.start[0] == self.end[0]:
            self.decks = [Deck(self.start[0], i)
                          for i in range(self.start[1], self.end[1] + 1)]
        if self.start[1] == self.end[1]:
            self.decks = [Deck(i, self.start[1])
                          for i in range(self.start[0], self.end[0] + 1)]

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is not None:
            deck.is_alive = False

        self.is_drowned = not any(deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = ships
        self.field = {}
        self.setup_field()

    def setup_field(self) -> None:
        for start, end in self.ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
