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
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = list()
        self.is_drowned = is_drowned
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(
            self,
            row: int,
            column: int
    ) -> Optional[Deck]:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(
            self,
            row: int,
            column: int
    ) -> None:
        if self.get_deck(row, column):
            self.get_deck(row, column).is_alive = False
            self.is_drowned = not any(
                deck.is_alive for deck in self.decks
            )


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = dict()
        for ship in ships:
            battleship = Ship(ship[0], ship[1])
            for deck in battleship.decks:
                self.field[(deck.row, deck.column)] = battleship

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
