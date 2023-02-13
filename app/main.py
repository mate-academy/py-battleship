from typing import Tuple, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: Tuple[int, int],
                 end: Tuple[int, int]
                 ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = False
        self.decks = []

        for row in range(self.start[0], self.end[0] + 1):
            for column in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck

    def fire(self, row: int, column: int) -> None:
        deck_of_ship = self.get_deck(row, column)
        if deck_of_ship is not None:
            deck_of_ship.is_alive = False
            for deck in self.decks:
                if deck.is_alive:
                    return
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = {}
        for ship in ships:
            ship = Ship(ship[0], ship[1])

            for deck in ship.decks:
                self.field[deck.row, deck.column] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        row, column = location

        if location in self.field:
            self.field[location].fire(row, column)
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
