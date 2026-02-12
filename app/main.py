from typing import List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"Deck({self.row}, {self.column}, {self.is_alive})"


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
        self.decks = self._create_decks()

    def _create_decks(self) -> List[Deck]:
        start_row, start_column = self.start
        end_row, end_column = self.end
        decks = []
        for row in range(min(start_row, end_row), max(start_row, end_row) + 1):
            for column in range(min(start_column, end_column),
                                max(start_column, end_column) + 1):
                decks.append(Deck(row, column))
        return decks

    def __repr__(self) -> str:
        return f"Ship({self.start}, {self.end}, {self.is_drowned})"

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True


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
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def __repr__(self) -> str:
        return f"Battleship({self.ships})"

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        row, column = location
        if (row, column) not in self.field:
            return "Miss!"
        ship = self.field[(row, column)]
        deck = ship.get_deck(row, column)
        deck.is_alive = False
        if all(not deck.is_alive for deck in ship.decks):
            ship.is_drowned = True
            return "Sunk!"
        return "Hit!"
