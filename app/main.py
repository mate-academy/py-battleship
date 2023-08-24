from typing import Union


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Union[Deck, None]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
        check = [not deck.is_alive for deck in self.decks]
        self.is_drowned = all(check)


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = []
        for ship in ships:
            self.ships.append(Ship(ship[0], ship[1], is_drowned=False))

        self.field = {
            (deck.row, deck.column): ship
            for ship in self.ships
            for deck in ship.decks
        }

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
