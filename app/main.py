from typing import Tuple


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

        if start[1] != end[1]:
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], col))
        elif start[0] != end[0]:
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, start[1]))
        else:
            self.decks.append(Deck(start[0], end[1]))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        self.is_drowned = all([not deck.is_alive for deck in self.decks])


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}

        for ship in ships:
            unit = Ship(ship[0], ship[1])
            if ship[0][0] != ship[1][0]:
                for row in range(ship[0][0], ship[1][0] + 1):
                    self.field[(ship[0][1], row)] = unit
            elif ship[0][1] != ship[1][1]:
                for col in range(ship[0][1], ship[1][1] + 1):
                    self.field[(ship[0][0], col)] = unit
            else:
                self.field[ship[0]] = unit

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
