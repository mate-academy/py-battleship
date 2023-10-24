from __future__ import annotations


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    @staticmethod
    def get_all_decks_between(deck1: Deck, deck2: Deck) -> list[Deck]:
        decks = []

        for row in range(deck1.row, deck2.row + 1):
            for column in range(deck1.column, deck2.column + 1):
                decks.append(Deck(row, column))

        return decks

    @staticmethod
    def from_tuple(deck_tuple: tuple[int, int]) -> Deck:
        return Deck(deck_tuple[0], deck_tuple[1])

    @staticmethod
    def to_tuple(deck: Deck) -> tuple[int, int]:
        return deck.row, deck.column

    def __repr__(self) -> str:
        return f"({self.row}, {self.column})"

    def __eq__(self, other: Deck | tuple[int, int]) -> bool:
        if isinstance(other, tuple):
            return self.row == other[0] and self.column == other[1]
        return self.row == other.row and self.column == other.column


class Ship:
    def __init__(self,
                 start: tuple[int, int],
                 end: tuple[int, int],
                 is_drowned: bool = False) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks = Deck.get_all_decks_between(
            Deck.from_tuple(start),
            Deck.from_tuple(end)
        )
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck == (row, column):
                return deck

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        self.get_deck(row, column).is_alive = False

        for deck in self.decks:
            if deck.is_alive:
                return
        self.is_drowned = True

    @staticmethod
    def from_tuple(ship_tuple: tuple[tuple]) -> Ship:
        return Ship(ship_tuple[0], ship_tuple[1])


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        for ship in ships:
            ship_cells = [Deck.to_tuple(deck)
                          for deck in Ship.from_tuple(ship).decks]
            value = Ship.from_tuple(ship)

            for cell in ship_cells:
                self.field[cell] = value

    def fire(self, location: tuple[int, int]) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field:
            self.field[location].fire(*location)
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
