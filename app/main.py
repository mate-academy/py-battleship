from typing import Tuple, List


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
            start: Tuple[int],
            end: Tuple[int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row=row, column=column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if (deck.row == row) and (deck.column == column):
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row=row, column=column)

        if deck is not None:
            deck.is_alive = False
            self.decks.remove(deck)

            if not self.decks:
                self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: List[Tuple]
    ) -> None:
        self.ships = ships
        self.field = {}
        self.create_field()

    def create_field(self) -> None:

        for coords in self.ships:
            ship = Ship(start=coords[0], end=coords[1])

            all_positions = [
                (x_coord, y_coord)
                for x_coord in range(ship.start[0], ship.end[0] + 1)
                for y_coord in range(ship.start[1], ship.end[1] + 1)
            ]

            for position in all_positions:
                self.field[position] = ship

    def fire(self, location: tuple) -> str:

        if location in self.field:
            ship = self.field[location]
            ship.fire(row=location[0], column=location[1])

            if ship.is_drowned:
                return "Sunk!"

            return "Hit!"

        return "Miss!"
