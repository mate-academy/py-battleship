from typing import Optional


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
            start: tuple[int],
            end: tuple[int],
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        for column in range(start[1], end[1] + 1):
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        hit_deck = self.get_deck(row, column)
        if hit_deck:
            hit_deck.is_alive = False

        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            self.ship = Ship(*ship)
            for deck in self.ship.decks:
                self.field[deck.row, deck.column] = self.ship

    def fire(self, location: tuple[int]) -> str:
        if location not in self.field:
            return "Miss!"
        else:
            self.field[location].fire(*location)
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
