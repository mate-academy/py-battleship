from typing import Any


class Deck:
    def __init__(self, row: Any, column: Any, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: list,
            end: list,
            is_drowned: bool = False
    ) -> None:
        r1, c1 = start
        r2, c2 = end
        self.is_drowned = is_drowned
        self.decks = []

        for row in range(min(r1, r2), max(r1, r2) + 1):
            for column in range(min(c1, c2), max(c1, c2) + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Any:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        decks = self.get_deck(row, column)
        if decks:
            decks.is_alive = False
        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        for start, end in ships:
            ship = Ship(start, end)

            for deck in ship.decks:
                cell_coordinated = (deck.row, deck.column)

                self.field[cell_coordinated] = ship

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"

        row, column = location
        ship = self.field[location]

        ship.fire(row, column)

        if ship.is_drowned:
            return "Sunk!"
        else:
            return "Hit!"
