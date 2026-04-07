from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


Location = Tuple[int, int]


@dataclass
class Deck:
    row: int
    column: int
    is_alive: bool = True

    def hit(self) -> None:
        self.is_alive = False


class Ship:
    def __init__(self, start: Location, end: Location) -> None:
        self.decks: List[Deck] = []
        self.is_drowned: bool = False

        self._build_decks(start, end)

    def _build_decks(self, start: Location, end: Location) -> None:
        row1, col1 = start
        row2, col2 = end

        if row1 != row2 and col1 != col2:
            raise ValueError("Ship must be horizontal or vertical")

        if row1 == row2:
            for column in range(min(col1, col2), max(col1, col2) + 1):
                self.decks.append(Deck(row1, column))
        else:
            for row in range(min(row1, row2), max(row1, row2) + 1):
                self.decks.append(Deck(row, col1))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is None or not deck.is_alive:
            return

        deck.hit()
        self._update_drowned_status()

    def _update_drowned_status(self) -> None:
        self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: List[Tuple[Location, Location]]) -> None:
        self.ships: List[Ship] = []
        self.field: Dict[Location, Ship] = {}

        self._build_field(ships)
        self._validate_field()

    def _build_field(self, ships: List[Tuple[Location, Location]]) -> None:
        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            self._add_ship_to_field(ship)

    def _add_ship_to_field(self, ship: Ship) -> None:
        for deck in ship.decks:
            location = (deck.row, deck.column)
            if location in self.field:
                raise ValueError("Ships overlap")

            self.field[location] = ship

    def fire(self, location: Location) -> str:
        ship = self.field.get(location)
        if ship is None:
            return "Miss!"

        row, column = location
        deck = ship.get_deck(row, column)

        if deck is not None and not deck.is_alive:
            return "Sunk!" if ship.is_drowned else "Miss!"

        ship.fire(row, column)

        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"

    def _validate_field(self) -> None:
        self._validate_ships_count()
        self._validate_ships_sizes()
        self._validate_no_touching()

    def _validate_ships_count(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("Invalid number of ships")

    def _validate_ships_sizes(self) -> None:
        expected = {1: 4, 2: 3, 3: 2, 4: 1}
        counts = {1: 0, 2: 0, 3: 0, 4: 0}

        for ship in self.ships:
            length = len(ship.decks)
            if length not in counts:
                raise ValueError("Invalid ship size")

            counts[length] += 1

        if counts != expected:
            raise ValueError("Invalid ships configuration")

    def _validate_no_touching(self) -> None:
        for (row, column), ship in self.field.items():
            for d_row in (-1, 0, 1):
                for d_column in (-1, 0, 1):
                    if d_row == 0 and d_column == 0:
                        continue

                    neighbor = (row + d_row, column + d_column)
                    other_ship = self.field.get(neighbor)

                    if other_ship is not None and other_ship is not ship:
                        raise ValueError("Ships are touching")

    def print_field(self) -> None:
        for row in range(10):
            line = []
            for column in range(10):
                line.append(self._cell_symbol(row, column))
            print(" ".join(line))

    def _cell_symbol(self, row: int, column: int) -> str:
        ship = self.field.get((row, column))
        if ship is None:
            return "~"

        deck = ship.get_deck(row, column)
        if deck is not None and deck.is_alive:
            return "□"

        if ship.is_drowned:
            return "x"
        return "*"
