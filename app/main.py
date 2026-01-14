from typing import List, Tuple, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row: int = row
        self.column: int = column
        self.is_alive: bool = is_alive

    def __repr__(self) -> str:
        return f"Deck({self.row}, {self.column}, " \
               f"{'Alive' if self.is_alive else 'Dead'})"


class Ship:
    def __init__(self, coordinates: List[Tuple[int, int]]) -> None:
        """Accepts a list of two tuples [(row1, col1), (row2, col2)]."""
        self.start: Tuple[int, int] = coordinates[0]
        self.end: Tuple[int, int] = coordinates[1]
        self.decks: List[Deck] = []

        if self.start[0] == self.end[0]:  # Horizontal ship
            for col in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], col))
        else:  # Vertical ship
            for row in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(row, self.start[1]))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return "Deck not found!"

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def __repr__(self) -> str:
        return f"Ship({self.decks})"


class Battleship:
    def __init__(self, ships: List[List[Tuple[int, int]]]) -> None:
        """Accepts a list of lists, where each sublist represents a ship."""
        self.ships: List[Ship] = []
        self.field: dict[Tuple[int, int], Ship] = {}

        for ship_coords in ships:
            ship = Ship(ship_coords)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: Tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            return ship.fire(*location)
        return "Miss!"

    def _validate_field(self) -> None:
        """Ensures ships are correctly placed with proper sizes."""
        ship_sizes: List[int] = [len(ship.decks) for ship in self.ships]
        expected: dict[int, int] = {1: 4, 2: 3, 3: 2, 4: 1}
        counts: dict[int, int] = {size: ship_sizes.count(size)
                                  for size in expected.keys()}

        if counts != expected:
            raise ValueError("Invalid ship configuration!")

    def print_field(self) -> None:
        grid: List[List[str]] = [["~" for _ in range(10)] for _ in range(10)]
        for (row, col), ship in self.field.items():
            deck = ship.get_deck(row, col)
            grid[row][col] = "□" if deck.is_alive else "x"

        for row in grid:
            print(" ".join(row))
