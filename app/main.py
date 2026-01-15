from typing import List, Tuple, Optional


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
        self.decks = []
        self.is_drowned = is_drowned
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: List[Tuple[int, int]]) -> None:
        self.field = {}
        for ship_start, ship_end in ships:
            ship = Ship(ship_start, ship_end)
            for dec in ship.decks:
                self.field[(dec.row, dec.column)] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def _validate_field(self) -> bool:
        for ship in self.ships:
            for deck in ship.decks:
                for i in range(deck.row - 1, deck.row + 2):
                    for _column in range(deck.column - 1, deck.column + 2):
                        if (
                            (i, _column) in self.field
                            and (i, _column) != (deck.row, deck.column)
                        ):
                            return False
