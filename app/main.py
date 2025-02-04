
"""
This module implements a simple Battleship game.

Classes:
    Deck: Represents a single deck (cell) of a ship.
    Ship: Represents a ship composed of multiple decks.
    Battleship: Represents the game board and manages the ships and firing
        logic.

Deck:
    Methods:
        __init__(row: int, column: int, is_alive: bool = True): Initializes a
            deck with its position and status.

Ship:
    Methods:
        __init__(start: tuple, end: tuple, is_drowned: bool = False):
            Initializes a ship with its start and end coordinates.
        build_decks(start: tuple, end: tuple) -> list: Static method to create
            a list of decks for the ship.
        get_deck(row: int, column: int) -> Deck: Finds and returns the deck at
            the specified position.
        fire(row: int, column: int) -> None: Changes the `is_alive` status of
            the deck and updates the `is_drowned` status if needed.

Battleship:
    Methods:
        __init__(ships: list) -> None: Initializes the game board with the
            given ships.
        place_ships(ships: list) -> dict: Static method to create a dictionary
            of ship positions.
        fire(location: tuple) -> str: Checks if the given location hits a ship
            and updates the ship's status accordingly.
"""


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    # Create decks and save them to a list `self.decks`
    def __init__(self, start: tuple, end: tuple,
                 is_drowned: bool = False) -> None:
        self.decks = self.build_decks(start, end)
        self.is_drowned = is_drowned

    @staticmethod
    def build_decks(start: tuple, end: tuple) -> list:
        # Create a list of decks for the ship
        decks = []
        if start[0] == end[0]:  # Horizontal ship
            for column in range(start[1], end[1] + 1):
                decks.append(Deck(start[0], column))
        elif start[1] == end[1]:  # Vertical ship
            for row in range(start[0], end[0] + 1):
                decks.append(Deck(row, start[1]))
        else:
            raise ValueError("Invalid ship coordinates: "
                             "Ships must be either horizontal or vertical.")
        return decks

    def get_deck(self, row: int, column: int) -> Deck:
        # Find the corresponding deck in the list
        return next(
            (deck for deck in self.decks
             if deck.row == row and deck.column == column), None)

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            # Update the `is_drowned` value if needed
            self.is_drowned = all(not d.is_alive for d in self.decks)


class Battleship:
    def __init__(self, ships: list) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = self.place_ships(ships)

    @staticmethod
    def place_ships(ships: list) -> dict:
        # Create a dict `field` and fill it with the ships
        return {coordinates: Ship(*coordinates) for coordinates in ships}

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        for ship in self.field.values():
            deck = ship.get_deck(location[0], location[1])
            if deck:
                ship.fire(location[0], location[1])
                return "Sunk!" if ship.is_drowned else "Hit!"
        return "Miss!"
