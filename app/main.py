from collections import defaultdict
from typing import List, Tuple


class Deck:
    def __init__(
        self,
        row: int,
        column: int,
        is_alive: bool = True,
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self,
        start: Tuple,
        end: Tuple,
        is_drowned: bool = False,
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]

    def get_deck(self, row: int, column: int) -> Deck:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            self.is_drowned = all(not deck.is_alive for deck in self.decks)
            return self.is_drowned
        else:
            return None


class Battleship:
    def __init__(self, ships: List[Tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = [Ship(ship[0], ship[1]) for ship in ships]

        self.field = {
            (deck.row, deck.column): ship
            for ship in self.ships
            for deck in ship.decks
        }

        self._validate_field()

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("There should be 10 ships on the field.")

        deck_count = defaultdict(int)
        for ship in self.ships:
            if 1 <= len(ship.decks) <= 4:
                deck_count[len(ship.decks)] += 1
            else:
                raise ValueError("Each ship should have 1 to 4 decks.")

        if deck_count.get(1) != 4:
            raise ValueError("There should be 4 single-deck ships.")
        elif deck_count.get(2) != 3:
            raise ValueError("There should be 3 double-deck ships.")
        elif deck_count.get(3) != 2:
            raise ValueError("There should be 2 three-deck ships.")
        elif deck_count.get(4) != 1:
            raise ValueError("There should be 1 four-deck ship.")

        # ships shouldn't be located in the neighboring cells
        # (even if cells are neighbors by diagonal).

    def __str__(self) -> str:
        """This function should print the field."""
        # ~ symbol for empty cells
        # □ symbol for alive decks.
        # * for hit decks of the alive ship
        # x for decks of the drowned ship

        output = [["~" for _ in range(10)] for _ in range(10)]

        for (row, column), ship in self.field.items():
            deck = ship.get_deck(row, column)
            if deck.is_alive:
                output[row][column] = "□"
            else:
                output[row][column] = "x" if ship.is_drowned else "*"

        return "\n".join("  ".join(row) for row in output)

    def fire(self, location: tuple) -> str:
        """This function should check whether the location is
        a key in the `self.field` If it is, then it should check
        if this cell is the last alive in the ship or not."""

        row, column = location

        if (row, column) in self.field:
            ship = self.field[(row, column)]
            if ship.fire(row, column):
                return "Sunk!"
            return "Hit!"
        return "Miss!"
