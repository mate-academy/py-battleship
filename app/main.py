from typing import List, Dict


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
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = self._create_decks(start, end)

    @staticmethod
    def _create_decks(start: tuple, end: tuple) -> List[Deck]:
        decks = []
        if start[0] == end[0]:
            for column in range(start[1], end[1] + 1):
                decks.append(Deck(start[0], column))
        else:
            for row in range(start[0], end[0] + 1):
                decks.append(Deck(row, start[1]))

        return decks

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: List[tuple]) -> None:
        self.field = self._create_ships(ships)

    @staticmethod
    def _create_ships(ships: List[tuple]) -> Dict[tuple, Ship]:
        field = {}
        for start, end in ships:
            ship = Ship(start, end)
            key = tuple([(deck.row, deck.column)for deck in ship.decks])
            field[key] = ship

        return field

    def fire(self, location: tuple) -> str:
        for locs, ship in self.field.items():
            if location in locs:
                ship.fire(*location)
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        field = ""
        ship_location = {
            location: ship
            for locations, ship in self.field.items()
            for location in locations
        }
        for row in range(10):
            for column in range(10):
                if (row, column) in ship_location:
                    ship = ship_location[row, column]
                    if ship.is_drowned:
                        field += "x    "
                    else:
                        deck = ship.get_deck(row, column)
                        field += "□    " if deck.is_alive else "*    "
                else:
                    field += "~    "
                if column == 9:
                    field += "\n"

        print(field)
