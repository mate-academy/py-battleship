from collections import Counter
from typing import Iterator


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.row, self.column


class Ship:
    def __init__(self, start: int, end: int, is_drowned: bool = False) -> None:
        # Create decks and save them to a list `self.decks`
        self.is_drowned = is_drowned
        self.decks = []
        start_row, start_column = start
        end_row, end_column = end

        if start_row != end_row and start_column != end_column:
            raise ValueError("Ship must be strictly horizontal or vertical.")
        if start_row == end_row:  # horizontal ship
            left_column, right_column = sorted((start_column, end_column))
            for column_index in range(left_column, right_column + 1):
                self.decks.append(Deck(start_row, column_index))
        else:  # vertical ship
            top_row, bottom_row = sorted((start_row, end_row))
            for row_index in range(top_row, bottom_row + 1):
                self.decks.append(Deck(row_index, start_column))

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def _update_is_drowned(self) -> None:
        self.is_drowned = all(not deck.is_alive for deck in self.decks)

    def fire(self, row: int, column: int) -> str | None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        if deck is None or not deck.is_alive:
            return None

        deck.is_alive = False
        self._update_is_drowned()
        return "Sunk!" if self.is_drowned else "Hit!"


class Battleship:
    def __init__(self, ships: list) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        self.ships = []
        for start, end in ships:
            ship = Ship(start, end)
            self._validate_in_bounds(ship)
            for deck in ship.decks:
                if deck.coordinates in self.field:
                    raise ValueError(f"Overlapping ships"
                                     f" at {deck.coordinates}")
                self.field[deck.coordinates] = ship
            self.ships.append(ship)

        self._validate_field()

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        row, col = location
        ship = self.field.get((row, col))
        if ship is None:
            return "Miss!"

        # Delegate to the ship; if already dead at this cell, treat as a miss.
        result = ship.fire(row, col)
        if result is None:
            return "Miss!"
        return result

    @staticmethod
    def _in_bounds(row: int, col: int) -> bool:
        return 0 <= row <= 9 and 0 <= col <= 9

    def _validate_in_bounds(self, ship: Ship) -> None:
        for deck in ship.decks:
            if not self._in_bounds(deck.row, deck.column):
                raise ValueError(f"Deck {deck.coordinates} is out "
                                 f"of bounds (0..9).")

    def _neighbors8(self, row: int, column: int) -> Iterator[tuple[int, int]]:
        """All 8 neighbors within bounds (no center)."""
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, column + dc
                if self._in_bounds(nr, nc):
                    yield (nr, nc)

    def _validate_field(self) -> None:
        """
        Checks after field creation:
        - total number of ships is 10;
        - size distribution: 4×1, 3×2, 2×3, 1×4;
        - ships are not adjacent even diagonally.
        """
        # 1) Count ships
        if len(self.ships) != 10:
            raise ValueError(f"Invalid number of ships: "
                             f"{len(self.ships)} (expected 10)")

        # 2) Size distribution
        sizes = Counter(len(size.decks) for size in self.ships)
        expected = {1: 4, 2: 3, 3: 2, 4: 1}
        # Reject unexpected sizes too
        unexpected_sizes = [key for key in sizes.keys() if key not in expected]
        if unexpected_sizes:
            raise ValueError(f"Unexpected ship size(s): {unexpected_sizes}; "
                             f"only sizes 1..4 allowed.")

        for size, need in expected.items():
            have = sizes.get(size, 0)
            if have != need:
                raise ValueError(f"Invalid count for size {size}: "
                                 f"have {have}, expected {need}")

        # 3) No adjacency (including diagonals)
        # For each deck, none of the 8-neighbors may belong
        # to a *different* ship.
        for (row, column), ship in self.field.items():
            for neighbor_row, neighbor_column in self._neighbors8(row, column):
                neighbor_ship = self.field.get((neighbor_row, neighbor_column))
                if neighbor_ship is not None and neighbor_ship is not ship:
                    raise ValueError(
                        f"Ships adjacent at {(row, column)} and "
                        f"{(neighbor_row, neighbor_column)} "
                        f"(adjacency is forbidden)."
                    )
